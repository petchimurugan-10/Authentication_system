import React, { useState } from 'react';
import { GoogleLogin } from 'react-google-login';
import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const { login, googleLogin } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await login(credentials);
    if (!result.success) {
      alert(result.error);
    }
  };

  const handleGoogleSuccess = async (response) => {
    const result = await googleLogin(response.tokenId);
    if (!result.success) {
      alert(result.error);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={credentials.email}
          onChange={(e) => setCredentials({...credentials, email: e.target.value})}
        />
        <input
          type="password"
          placeholder="Password"
          value={credentials.password}
          onChange={(e) => setCredentials({...credentials, password: e.target.value})}
        />
        <button type="submit">Login</button>
      </form>
      
      <GoogleLogin
        clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}
        buttonText="Login with Google"
        onSuccess={handleGoogleSuccess}
        onFailure={(error) => console.log(error)}
        cookiePolicy={'single_host_origin'}
      />
    </div>
  );
};

export default Login;
