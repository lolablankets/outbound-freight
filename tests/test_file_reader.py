"""
Test module for file reading and dynamic header detection functionality.

Following TDD RED-GREEN-REFACTOR:
- Tests written FIRST to define expected behavior
- Implementation follows to make tests pass
- Tests validate against actual sample files in data/2025/08/
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import os

from outbound_freight.file_reader import FileReader, FileReaderError


class TestFileReaderBasics:
    """Test basic file reading functionality."""
    
    def test_read_excel_file_returns_dataframe(self):
        """Test that reading an Excel file returns a pandas DataFrame."""
        reader = FileReader()
        result = reader.read_file("data/2025/08/FDX_20250802_LOL509.xlsx")
        
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert len(result.columns) > 0
    
    def test_read_csv_file_returns_dataframe(self):
        """Test that reading a CSV file returns a pandas DataFrame."""
        # Create a test CSV file
        test_csv_content = """Name,Age,City
John,25,New York
Jane,30,Boston"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(test_csv_content)
            temp_path = f.name
        
        try:
            reader = FileReader()
            result = reader.read_file(temp_path)
            
            assert isinstance(result, pd.DataFrame)
            assert not result.empty
            assert list(result.columns) == ['Name', 'Age', 'City']
            assert len(result) == 2
        finally:
            os.unlink(temp_path)
    
    def test_unsupported_file_format_raises_error(self):
        """Test that unsupported file formats raise appropriate error."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"some text content")
            temp_path = f.name
        
        try:
            reader = FileReader()
            with pytest.raises(FileReaderError, match="Unsupported file format"):
                reader.read_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_nonexistent_file_raises_error(self):
        """Test that non-existent files raise appropriate error."""
        reader = FileReader()
        with pytest.raises(FileReaderError, match="File not found"):
            reader.read_file("nonexistent_file.xlsx")


class TestHeaderDetection:
    """Test dynamic header detection functionality."""
    
    def test_detects_headers_in_row_1(self):
        """Test header detection when headers are in row 1 (standard case)."""
        # Create Excel file with headers in row 1 (with enough columns)
        test_data = pd.DataFrame({
            'Column A': [1, 2, 3],
            'Column B': [4, 5, 6],
            'Column C': [7, 8, 9],
            'Column D': [10, 11, 12]
        })
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        test_data.to_excel(temp_path, index=False)
        
        try:
            reader = FileReader()
            result = reader.read_file(temp_path)
            
            assert list(result.columns) == ['Column A', 'Column B', 'Column C']
            assert len(result) == 3
        finally:
            os.unlink(temp_path)
    
    def test_detects_headers_in_row_4_fedex_format(self):
        """Test header detection for FedEx format (headers in row 4)."""
        reader = FileReader()
        result = reader.read_file("data/2025/08/FDX_20250802_LOL509.xlsx")
        
        # FedEx files should have these key columns
        expected_columns = [
            'Tracking Number', 'Invoice Date', 'Ship Date', 
            'Service Type', 'Actual Weight'
        ]
        
        for col in expected_columns:
            assert col in result.columns, f"Expected column '{col}' not found"
        
        # Should have data rows (not just headers)
        assert len(result) > 0
    
    def test_detects_headers_in_row_3_ups_format(self):
        """Test header detection for UPS format (headers in row 3)."""
        reader = FileReader()
        result = reader.read_file("data/2025/08/UPS_LOL509_08022025.xlsx")
        
        # UPS files should have these key columns
        expected_columns = [
            'Carrier Invoice Date', 'Tracking Number', 
            'Reference 1', 'Reference 2'
        ]
        
        for col in expected_columns:
            assert col in result.columns, f"Expected column '{col}' not found"
        
        # Should have data rows (not just headers)
        assert len(result) > 0
    
    def test_header_detection_with_merged_cells(self):
        """Test header detection with merged cells and formatting."""
        # This will be tested against actual sample files
        reader = FileReader()
        
        # Should not crash on files with merged cells
        result = reader.read_file("data/2025/08/FDX_20250802_LOL509.xlsx")
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_missing_headers_raises_error(self):
        """Test that files without detectable headers raise error."""
        # Create Excel file with no clear headers (all numeric data)
        test_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        df = pd.DataFrame(test_data)
        df.to_excel(temp_path, index=False, header=False)
        
        try:
            reader = FileReader()
            with pytest.raises(FileReaderError, match="No headers detected"):
                reader.read_file(temp_path)
        finally:
            os.unlink(temp_path)


class TestErrorHandling:
    """Test error handling for various file conditions."""
    
    def test_empty_file_handling(self):
        """Test handling of empty Excel files."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        # Create empty Excel file
        pd.DataFrame().to_excel(temp_path, index=False)
        
        try:
            reader = FileReader()
            with pytest.raises(FileReaderError, match="File is empty"):
                reader.read_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_corrupted_file_handling(self):
        """Test handling of corrupted Excel files."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            f.write(b"this is not a valid Excel file")
            temp_path = f.name
        
        try:
            reader = FileReader()
            with pytest.raises(FileReaderError, match="corrupted or invalid"):
                reader.read_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_different_csv_encodings(self):
        """Test CSV files with different encodings."""
        # Test UTF-8 encoding
        test_content = "Name,City\nJohn,New York\nJané,São Paulo"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                       encoding='utf-8', delete=False) as f:
            f.write(test_content)
            temp_path = f.name
        
        try:
            reader = FileReader()
            result = reader.read_file(temp_path)
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
            assert 'Jané' in result['Name'].values
        finally:
            os.unlink(temp_path)


class TestSampleFileIntegration:
    """Test against all actual sample files in data/2025/08/."""
    
    @pytest.fixture
    def sample_files(self):
        """Get list of all sample files."""
        sample_dir = Path("data/2025/08/")
        return list(sample_dir.glob("*.xlsx"))
    
    def test_all_sample_files_readable(self, sample_files):
        """Test that all sample files can be read without errors."""
        reader = FileReader()
        
        assert len(sample_files) == 10, f"Expected 10 sample files, found {len(sample_files)}"
        
        for file_path in sample_files:
            # Should not raise any exceptions
            result = reader.read_file(str(file_path))
            
            # Basic validations
            assert isinstance(result, pd.DataFrame)
            assert not result.empty, f"File {file_path.name} returned empty DataFrame"
            assert len(result.columns) > 0, f"File {file_path.name} has no columns"
            assert len(result) > 0, f"File {file_path.name} has no data rows"
    
    def test_fedex_files_have_required_structure(self, sample_files):
        """Test that FedEx files have expected column structure."""
        reader = FileReader()
        fedex_files = [f for f in sample_files if 'FDX' in f.name]
        
        assert len(fedex_files) == 5, f"Expected 5 FedEx files, found {len(fedex_files)}"
        
        required_columns = ['Tracking Number', 'Invoice Date']
        
        for file_path in fedex_files:
            result = reader.read_file(str(file_path))
            
            for col in required_columns:
                assert col in result.columns, f"FedEx file {file_path.name} missing column '{col}'"
    
    def test_ups_files_have_required_structure(self, sample_files):
        """Test that UPS files have expected column structure."""
        reader = FileReader()
        ups_files = [f for f in sample_files if 'UPS' in f.name]
        
        assert len(ups_files) == 5, f"Expected 5 UPS files, found {len(ups_files)}"
        
        required_columns = ['Tracking Number', 'Carrier Invoice Date']
        
        for file_path in ups_files:
            result = reader.read_file(str(file_path))
            
            for col in required_columns:
                assert col in result.columns, f"UPS file {file_path.name} missing column '{col}'"
    
    def test_sample_files_return_consistent_data_types(self, sample_files):
        """Test that sample files return DataFrames with reasonable data types."""
        reader = FileReader()
        
        for file_path in sample_files:
            result = reader.read_file(str(file_path))
            
            # Should have mixed data types (not all object/string)
            dtypes = result.dtypes
            assert len(set(dtypes)) > 1, f"File {file_path.name} has only one data type"
            
            # Should not have ALL columns be all NaN (but some empty columns are normal)
            all_nan_columns = [col for col in result.columns if result[col].isna().all()]
            assert len(all_nan_columns) < len(result.columns) * 0.5, f"Too many empty columns in {file_path.name}: {all_nan_columns}"


class TestFileReaderConfiguration:
    """Test FileReader configuration and options."""
    
    def test_max_header_search_rows_configurable(self):
        """Test that maximum header search rows is configurable."""
        reader = FileReader(max_header_rows=5)
        
        # Should still work with sample files
        result = reader.read_file("data/2025/08/FDX_20250802_LOL509.xlsx")
        assert isinstance(result, pd.DataFrame)
    
    def test_file_reader_preserves_data_integrity(self):
        """Test that file reader doesn't corrupt data during reading."""
        reader = FileReader()
        
        # Read the same file twice
        result1 = reader.read_file("data/2025/08/FDX_20250802_LOL509.xlsx")
        result2 = reader.read_file("data/2025/08/FDX_20250802_LOL509.xlsx")
        
        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2)