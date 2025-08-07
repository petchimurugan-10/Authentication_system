import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  const login = async (credentials) => {
    try {
      const response = await axios.post('/auth/login', credentials);
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      
      // Decode and set user info
      const userResponse = await axios.get('/user/profile', {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      setUser(userResponse.data.user);
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response.data.error };
    }
  };

  const googleLogin = async (tokenId) => {
    try {
      const response = await axios.post('/auth/oauth/google', { token: tokenId });
      const { access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      setToken(access_token);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.response.data.error };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    login,
    googleLogin,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
