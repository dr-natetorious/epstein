"""Email parser for extracting and analyzing email data from various formats."""

import email
import os
import mailbox
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class EmailParser:
    """Parse emails from various formats (EML, MBOX, PST)."""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize the email parser.
        
        Args:
            data_dir: Directory containing email files
        """
        self.data_dir = Path(data_dir) if data_dir else None
        self.emails = []
        
    def parse_eml_file(self, filepath: str) -> Dict[str, Any]:
        """
        Parse a single EML file.
        
        Args:
            filepath: Path to the EML file
            
        Returns:
            Dictionary containing email metadata and content
        """
        with open(filepath, 'rb') as f:
            msg = email.message_from_binary_file(f)
            
        return self._extract_email_data(msg)
    
    def parse_mbox(self, mbox_path: str) -> List[Dict[str, Any]]:
        """
        Parse an MBOX file.
        
        Args:
            mbox_path: Path to the MBOX file
            
        Returns:
            List of dictionaries containing email data
        """
        mbox = mailbox.mbox(mbox_path)
        emails = []
        
        for message in mbox:
            email_data = self._extract_email_data(message)
            emails.append(email_data)
            
        self.emails.extend(emails)
        return emails
    
    def parse_directory(self, directory: str, pattern: str = "*.eml") -> List[Dict[str, Any]]:
        """
        Parse all email files in a directory.
        
        Args:
            directory: Directory path
            pattern: File pattern to match (default: *.eml)
            
        Returns:
            List of dictionaries containing email data
        """
        dir_path = Path(directory)
        emails = []
        
        for filepath in dir_path.glob(pattern):
            if filepath.is_file():
                try:
                    email_data = self.parse_eml_file(str(filepath))
                    emails.append(email_data)
                except Exception as e:
                    print(f"Error parsing {filepath}: {e}")
                    
        self.emails.extend(emails)
        return emails
    
    def _extract_email_data(self, msg: email.message.Message) -> Dict[str, Any]:
        """
        Extract relevant data from an email message.
        
        Args:
            msg: Email message object
            
        Returns:
            Dictionary containing extracted email data
        """
        # Extract basic headers
        data = {
            'from': msg.get('From', ''),
            'to': msg.get('To', ''),
            'cc': msg.get('Cc', ''),
            'bcc': msg.get('Bcc', ''),
            'subject': msg.get('Subject', ''),
            'date': msg.get('Date', ''),
            'message_id': msg.get('Message-ID', ''),
        }
        
        # Parse date
        date_str = msg.get('Date', '')
        if date_str:
            try:
                data['parsed_date'] = email.utils.parsedate_to_datetime(date_str)
            except Exception:
                data['parsed_date'] = None
        else:
            data['parsed_date'] = None
        
        # Extract body
        body_parts = []
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                # Extract text parts
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body_parts.append(part.get_payload(decode=True).decode('utf-8', errors='ignore'))
                    except Exception:
                        pass
                        
                # Track attachments
                elif "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append({
                            'filename': filename,
                            'content_type': content_type,
                            'size': len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0
                        })
        else:
            try:
                body = msg.get_payload(decode=True)
                if body:
                    body_parts.append(body.decode('utf-8', errors='ignore'))
            except Exception:
                pass
        
        data['body'] = '\n'.join(body_parts)
        data['attachments'] = attachments
        data['attachment_count'] = len(attachments)
        
        return data
    
    def get_email_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about parsed emails.
        
        Returns:
            Dictionary containing email statistics
        """
        if not self.emails:
            return {
                'total_emails': 0,
                'error': 'No emails have been parsed yet'
            }
        
        # Extract sender domains
        sender_domains = []
        for email_data in self.emails:
            from_addr = email_data.get('from', '')
            match = re.search(r'@([\w\.-]+)', from_addr)
            if match:
                sender_domains.append(match.group(1))
        
        # Count attachments
        total_attachments = sum(email_data.get('attachment_count', 0) for email_data in self.emails)
        
        # Find date range
        dates = [email_data.get('parsed_date') for email_data in self.emails if email_data.get('parsed_date')]
        date_range = {}
        if dates:
            date_range = {
                'earliest': min(dates),
                'latest': max(dates)
            }
        
        return {
            'total_emails': len(self.emails),
            'total_attachments': total_attachments,
            'unique_sender_domains': len(set(sender_domains)),
            'date_range': date_range
        }
    
    def search_emails(self, keyword: str, field: str = 'body') -> List[Dict[str, Any]]:
        """
        Search emails for a keyword.
        
        Args:
            keyword: Keyword to search for
            field: Field to search in (body, subject, from, to)
            
        Returns:
            List of matching emails
        """
        keyword_lower = keyword.lower()
        results = []
        
        for email_data in self.emails:
            field_value = str(email_data.get(field, '')).lower()
            if keyword_lower in field_value:
                results.append(email_data)
                
        return results
