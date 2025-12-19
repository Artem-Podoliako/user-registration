"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional


class RegisterRequest(BaseModel):
    """Schema for user registration request."""
    
    login: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=8)
    
    @field_validator('login')
    @classmethod
    def validate_login(cls, v: str) -> str:
        """Validate login format: letters, numbers, dots, underscores, hyphens."""
        if not re.match(r'^[a-zA-Z0-9._-]+$', v):
            raise ValueError('Login must contain only letters, numbers, dots, underscores, or hyphens')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class RegisterResponse(BaseModel):
    """Schema for registration response."""
    
    message: str


class ErrorResponse(BaseModel):
    """Schema for error response."""
    
    detail: str

