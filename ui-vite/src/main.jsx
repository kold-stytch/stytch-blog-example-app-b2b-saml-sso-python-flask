import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

import { StytchB2BProvider } from '@stytch/react/b2b';
import { StytchB2BHeadlessClient } from '@stytch/vanilla-js/b2b/headless';

const stytch = new StytchB2BHeadlessClient(
  import.meta.env.VITE_STYTCH_PUBLIC_TOKEN, // or process.env.STYTCH_PUBLIC_TOKEN for non-Vite based projects
);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <StytchB2BProvider stytch={stytch}>
      <App />
    </StytchB2BProvider>
  </React.StrictMode>
)
