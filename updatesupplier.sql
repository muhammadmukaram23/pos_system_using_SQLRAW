USE pos_system;
ALTER TABLE tblsupplier 
ADD COLUMN contact_person VARCHAR(50) AFTER supplier_email,
ADD COLUMN bank_account_name VARCHAR(50) AFTER contact_person,
ADD COLUMN bank_account_number VARCHAR(25) AFTER bank_account_name;

-- Update existing supplier records with sample data (optional)
UPDATE tblsupplier SET 
    contact_person = 'John Smith',
    bank_account_name = 'ABC Electronics Bank Account',
    bank_account_number = '1234567890'
WHERE supplier_code = 'SUP001';

UPDATE tblsupplier SET 
    contact_person = 'Sarah Johnson',
    bank_account_name = 'XYZ Furniture Bank Account',
    bank_account_number = '2345678901'
WHERE supplier_code = 'SUP002';

UPDATE tblsupplier SET 
    contact_person = 'Mike Davis',
    bank_account_name = 'Office World Bank Account',
    bank_account_number = '3456789012'
WHERE supplier_code = 'SUP003';

-- Show the updated table structure
DESCRIBE tblsupplier; 