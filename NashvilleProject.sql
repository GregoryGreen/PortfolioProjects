-- Standardize Date Format

ALTER Table NashvilleHousingData
Add SaleDateConverted Date;

UPDATE NashvilleHousingData 
Set SaleDateConverted = CONVERT (Date, SaleDate);

SELECT *
From NashvilleHousingData;


-- Populate PropertyAddress data: joining the table to itself using UniqueID and ParcelID; to fill out the Null values

SELECT *
From NashvilleHousingData
order by ParcelID;


SELECT a.ParcelID , a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
From NashvilleHousingData a
JOIN NashvilleHousingData b    
	on a.ParcelID = b.ParcelID
    and a.[UniqueID ]  != b.[UniqueID ]
Where a.PropertyAddress is NULL;

UPDATE a 
Set PropertyAddress = COALESCE(a.PropertyAddress, b.PropertyAddress) 
From NashvilleHousingData a
JOIN NashvilleHousingData b    
	on a.ParcelID = b.ParcelID
    and a.[UniqueID ]  != b.[UniqueID ]
Where a.PropertyAddress is NULL;


-- Breaking out Address into Individual Columns (Address, City, State)

SELECT PropertyAddress 
From NashvilleHousingData
--order by ParcelID;

SELECT 
SUBSTRING(PropertyAddress, 1, CHARINDEX (',', PropertyAddress) -1 ) as Address,
SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) +1 , LEN(PropertyAddress)) as Address
From NashvilleHousingData;

Alter Table NashvilleHousingData 
Add PropertySplitAddress Varchar(255);

Update NashvilleHousingData
Set PropertySplitAddress = SUBSTRING(PropertyAddress, -1 , CHARINDEX (',', PropertyAddress))

Alter Table NashvilleHousingData 
Add PropertySplitCity varchar(255);

Update NashvilleHousingData
Set PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) +1 , LEN(PropertyAddress))

SELECT *
From NashvilleHousingData;

-- Using Parsename: more effient way of splitting the column

SELECT OwnerAddress
From NashvilleHousingData;

SELECT
Parsename(REPLACE(OwnerAddress, ',', '.') , 3),
Parsename(REPLACE(OwnerAddress, ',', '.') , 2),
Parsename(REPLACE(OwnerAddress, ',', '.') , 1)
From NashvilleHousingData;

Alter Table NashvilleHousingData 
Add OwnerSplitAddress Varchar(255);

Update NashvilleHousingData
Set OwnerSplitAddress = Parsename(REPLACE(OwnerAddress, ',', '.') , 3)

Alter Table NashvilleHousingData 
Add OwnerSplitCity varchar(255);

Update NashvilleHousingData
Set OwnerSplitCity = Parsename(REPLACE(OwnerAddress, ',', '.') , 2)

Alter Table NashvilleHousingData 
Add OwnerSplitState varchar(255);

Update NashvilleHousingData
Set OwnerSplitState = Parsename(REPLACE(OwnerAddress, ',', '.') , 1)

Select *
From NashvilleHousingData;

-- Change Y and N to Yes and No in "SoldAsVacant" column

Select DISTINCT(SoldAsVacant), COUNT(SoldAsVacant)
From NashvilleHousingData
Group by SoldAsVacant 
order by 2;

Select SoldAsVacant,
	Case When SoldAsVacant = 'Y' THEN 'Yes'
	 	 When SoldAsVacant = 'N' THEN 'No'
	 	 ELSE SoldAsVacant
	     End
From NashvilleHousingData;

Update NashvilleHousingData 
Set SoldAsVacant = Case When SoldAsVacant = 'Y' THEN 'Yes'
	 	 When SoldAsVacant = 'N' THEN 'No'
	 	 ELSE SoldAsVacant
	     End
	     
-- Remove Duplicates: using a combination of row_num, CTE, and windows function Partion by (dividing row set into smaller parts)

WITH RowNumCTE AS(
Select *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY
					UniqueID
					) row_num

From NashvilleHousingData
--order by ParcelID
)
Select *
From RowNumCTE
Where row_num > 1
Order by PropertyAddress

-- Delete Unused Columns

Select *
From NashvilleHousingData

Alter Table NashvilleHousingData
Drop Column OwnerAddress, TaxDistrict, PropertyAddress

Alter Table NashvilleHousingData
Drop Column SaleDate
