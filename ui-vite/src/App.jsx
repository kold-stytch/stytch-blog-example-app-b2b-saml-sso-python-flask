import { Button, Container } from '@mui/material';
import { useStytchB2BClient, useStytchMemberSession } from '@stytch/react/b2b';
import React, { useCallback, useEffect, useState } from 'react';
import { Route, Routes, useParams } from 'react-router-dom';
import './App.css';
import ProductsList from './ProductsList';

function B2BLogin() {
  const { orgId } = useParams();
  const [orgName, setOrgName] = useState('');
  const [orgUrl, setOrgUrl] = useState('');

  useEffect(() => {
    fetch(`http://localhost:3000/org/${orgId}`)
      .then(res => res.json())
      .then(data => {
        console.log(data)
        setOrgName(data.org_name)
        setOrgUrl(data.sso_url)
      })
      .catch(error => console.error('Error fetching org data:', error));
  }, [orgId]);

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">
          Continue to {orgName}
        </h2>
        <a href={orgUrl} className="login-link">
          Continue with SAML SSO
        </a>
      </div>
    </div>
  );
}

function Home() {
  return <p>Visit /org/:orgId to continue replacing your orgId with the one set in the Stytch Dashboard (e.g. /org/test-org)</p>;
}

function App() {
  const stytch = useStytchB2BClient();
  const { session } = useStytchMemberSession();

  const logout = useCallback(() => {
    stytch.session.revoke();
  }, [stytch]);

  return (
    <Container>
      {session && (
        <>
        <Button
          variant="outlined"
          color="secondary"
          onClick={logout}
          sx={{ position: "absolute", top: 16, right: 16 }}
        >
          Sign Out
        </Button>
      </>
      )}

      <Routes>
        <Route path="/org/:orgId" element={<B2BLogin />} />
        <Route path="/" element={session ? <ProductsList /> : <Home />} />
      </Routes>
    </Container>
  );
}

export default App;
