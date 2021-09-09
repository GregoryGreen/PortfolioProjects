SELECT *
From CovidDeaths 
order by 3,4;

SELECT *
From CovidVaccinations
order by 3, 4;


--Looking at total cases vs total deaths
--Shows likelihood of dying if contract virus (in US)
Select Location, date, total_cases,  total_deaths, (total_deaths  * 1.0 / total_cases)*100 as DeathPrecentage
From CovidDeaths
Where location like '%states%'
order by 1,2;

--total cases vs population
--Shows what percentage of population got Covid
Select Location, date, total_cases,  population, (total_cases*1.0  / population)*100 as PercentPopulationInfected
From CovidDeaths
Where location like '%states%'
order by 1, 2;

-- Countries with Highest Infection Rate compared to Population
Select Location,  population, Max(total_cases) as HighestInfectionCount, Max( (total_cases*1.0  / population))*100 as PercentPopulationInfected
From CovidDeaths
GROUP by location, population
order by PercentPopulationInfected DESC;


-- Showing countries with highest death count per population
SELECT Location, Max(cast(total_deaths as int)) as TotalDeathCount
From CovidDeaths
Where continent is not NULL
Group by location
Order by TotalDeathCount desc;

-- Showing contintents with the highest death count per population
SELECT continent, Max(cast(total_deaths as int)) as TotalDeathCount
From CovidDeaths
Where continent is  not NULL
Group by continent
Order by TotalDeathCount desc;

--Global Numbers
Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as int)) as total_deaths, SUM(cast(new_deaths  as int))/SUM(New_Cases * 1.0)*100 as DeathPercentage
From CovidDeaths
--Where location like '%states%'
where continent is not null 
--Group By date
order by 1,2;

--Total Population vs Vaccinations
--Percentage of Population that received at least one Covid Vaccine
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, sum(CAST(vac.new_vaccinations as INT)) Over (PARTITION by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
From CovidDeaths dea
Join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
WHERE dea.continent is not NULL
order by  2, 3;

-- Using CTE (common table expression) to perform Calculation on Partition By in previous query
With PopvsVac (continent, location,date, population, new_vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(CAST(vac.new_vaccinations as INT)) Over (PARTITION by dea.location Order by dea.location, dea.date) as RollingPeopleVaccinated
From CovidDeaths dea
Join CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
WHERE dea.continent is not NULL
--order by  2, 3
)
SELECT *, (RollingPeopleVaccinated/Population)*100
From PopvsVac


--Using Temp Table to perform Calculation on Partition By in previous query

DROP Table if exists PercentPopulationVaccinated
Create Table PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, SUM(CAST(int,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
order by 2,3

Select *,(RollingPeopleVaccinated/Population)*100
From PercentPopulationVaccinated


-- Creating View to store data for later visualizations

Create View PercentPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations as int)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
,(RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 