import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';

// Mock the AuthContext directly
import { AuthContext } from '../context/AuthContext';
import LoginPage from '../pages/LoginPage';

const mockAuth = {
  user: null,
  loading: false,
  login: () => {},
  logout: () => {}
};

describe('LoginPage', () => {
  it('renders username input', () => {
    render(
      <BrowserRouter>
        <AuthContext.Provider value={mockAuth}>
          <LoginPage />
        </AuthContext.Provider>
      </BrowserRouter>
    );
    const input = screen.getByPlaceholderText(/username/i);
    expect(input).toBeInTheDocument();
  });
});