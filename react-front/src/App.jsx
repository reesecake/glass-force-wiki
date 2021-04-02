import './App.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import SiteNav from './Components/SiteNav';
import Charousel from './Components/Character/Charousel';
import Container from 'react-bootstrap/Container';

function App() {
  return (
    <>
      <div className="site-nav">
        <SiteNav />
      </div>
      <Container className="content-container">
        <div className="charousel-container">
          <Charousel />
        </div>
      </Container>
    </>
  );
}

export default App;
