"""File processing utilities for PitchOS."""

import io
import PyPDF2
import docx
from typing import Optional

class FileProcessor:
    """Handles file upload and text extraction."""
    
    def __init__(self):
        """Initialize file processor."""
        pass
    
    def process_uploaded_file(self, uploaded_file) -> Optional[str]:
        """Process uploaded file and extract text content."""
        
        if uploaded_file is None:
            return None
        
        file_type = uploaded_file.type
        file_content = ""
        
        try:
            if file_type == "application/pdf":
                file_content = self._extract_pdf_text(uploaded_file)
            elif file_type == "text/plain":
                file_content = self._extract_text_file(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                file_content = self._extract_docx_text(uploaded_file)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            return file_content
            
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
    
    def _extract_pdf_text(self, uploaded_file) -> str:
        """Extract text from PDF file."""
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    
    def _extract_text_file(self, uploaded_file) -> str:
        """Extract text from plain text file."""
        return uploaded_file.read().decode('utf-8')
    
    def _extract_docx_text(self, uploaded_file) -> str:
        """Extract text from Word document."""
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        
        return text.strip()
    
    def validate_content(self, content: str) -> bool:
        """Validate that content is suitable for analysis."""
        
        if not content or len(content.strip()) < 100:
            return False
        
        # Check for minimum required elements
        content_lower = content.lower()
        required_elements = ['problem', 'solution', 'market', 'business']
        
        found_elements = sum(1 for element in required_elements if element in content_lower)
        
        return found_elements >= 2  # At least 2 key elements should be present
    
    def clean_content(self, content: str) -> str:
        """Clean and normalize content for analysis."""
        
        # Remove excessive whitespace
        content = ' '.join(content.split())
        
        # Remove special characters that might interfere with analysis
        content = content.replace('\x00', '')  # Remove null characters
        
        # Limit content length to prevent API limits
        max_length = 10000  # Adjust based on API limits
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        return content
