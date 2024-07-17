import { useStytchMember } from '@stytch/react/b2b';
import React from 'react';
import './App.css';

function App() {
  const { member } = useStytchMember();

  // react router to get org slug from url and fetch organization using 
  return (
    <>
    <h1>Hello {member?.name}</h1>
    </>
  )
}

export default App
