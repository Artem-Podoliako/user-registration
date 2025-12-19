/** API client for backend communication */
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface RegisterRequest {
  login: string;
  password: string;
}

export interface RegisterResponse {
  message: string;
}

export interface ErrorResponse {
  detail: string | Array<{ loc: string[]; msg: string; type: string }>;
}

export const registerUser = async (
  login: string,
  password: string
): Promise<RegisterResponse> => {
  const response = await axios.post<RegisterResponse>(
    `${API_URL}/api/register`,
    { login, password },
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
};

