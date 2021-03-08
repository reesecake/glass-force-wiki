import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import logo from '../Assets/brand/d&d_logo_amp.png';

const SiteNav = (props) => {
  return (
    <Navbar bg="dark" expand="lg" variant="dark">
      <Navbar.Brand href="#home">
        <img
          src={logo}
          alt=""
          width="50"
          height="50"
          class="d-inline-block align-center"
        />
        Glass Force
      </Navbar.Brand>
      <Navbar.Toggle/>
      <Navbar.Collapse>
        <Nav>
          <Nav.Link href="#about">About</Nav.Link>
          <NavDropdown title="Characters">
            <NavDropdown.Item href="#action/1">Add a Character</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/2">All Characters</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title="Locations">
            <NavDropdown.Item href="#action/1">Trollskull Manor</NavDropdown.Item>
            <NavDropdown.Item href="#action/2">Yawning Maw</NavDropdown.Item>
            <NavDropdown.Item href="#action/3">Add a Location</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/4">All Locations</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title="Session Entries">
            <NavDropdown.Item href="#action/1">Most Recent</NavDropdown.Item>
            <NavDropdown.Item href="#action/2">Create New Entries</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/4">All Entries</NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <Nav class="ml-auto">
          <Nav.Link href="#login" >Login</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  )
}

export default SiteNav;
