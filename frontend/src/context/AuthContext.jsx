import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiService } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('plantcare_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [loading, setLoading] = useState(false);
  const [authStatus, setAuthStatus] = useState(null);

  useEffect(() => {
    apiService.getAuthStatus()
      .then(res => setAuthStatus(res.data))
      .catch(() => setAuthStatus({ mode: 'offline', firebase_connected: false }));
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const res = await apiService.login(email, password);
      if (res.success && res.user) {
        setUser(res.user);
        localStorage.setItem('plantcare_user', JSON.stringify(res.user));
        return { success: true };
      }
      return { success: false, error: res.error || 'Login failed' };
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Login failed';
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, password, displayName) => {
    setLoading(true);
    try {
      const res = await apiService.register(email, password, displayName);
      if (res.success && res.user) {
        setUser(res.user);
        localStorage.setItem('plantcare_user', JSON.stringify(res.user));
        return { success: true };
      }
      return { success: false, error: res.error || 'Registration failed' };
    } catch (err) {
      const errorMsg = err.response?.data?.error || err.message || 'Registration failed';
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('plantcare_user');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, authStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

