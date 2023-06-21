import { useState, useContext } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Modal from 'react-bootstrap/Modal';
import AuthContext from '../context/AuthContext';

function ChangePassModal() {
  let { logout } = useContext(AuthContext);

  const [show, setShow] = useState(false);
  const [showPass, setShowPass] = useState(false);
  const [showPass2, setShowPass2] = useState(false);
  const [errorPass, setErrorPass] = useState(null);

  const handleClose = () => {
    setShow(false);
    setErrorPass(null);
  }
  const handleShow = () => setShow(true);

  const handleShowPass = () => setShowPass(!showPass);
  const handleShowPass2 = () => setShowPass2(!showPass2);

  let changePasswordRequest = async (e) => {
    e.preventDefault();

    // Change password
    let response = await fetch('/api/user/update-password', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        'old_password': e.target.old_password.value,
        'new_password': e.target.new_password.value
      })
    });

    if (!response.ok){
      setErrorPass('Aktualne hasło jest nieprawidłowe');
    };
    if (response.ok){
      // Logout
      handleClose();
      logout();
    }
  };

  return (
    <>
      <Button variant="warning" onClick={handleShow} style={{maxWidth: 200}}>
        Zmień hasło
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Zmaina hasła</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={changePasswordRequest}>
            <InputGroup className="mb-3">
              <Form.Control
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                placeholder="Aktualne hasło"
                type={showPass ? "text" : "password"}
                name='old_password'
                className={errorPass ? "is-invalid" : ""}
                required
              />
              <InputGroup.Text id="inputGroup-sizing-default" onClick={handleShowPass}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                  <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                  <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                </svg>
              </InputGroup.Text>
              {errorPass && <div className="invalid-feedback">{errorPass}</div> }
            </InputGroup>

            <InputGroup className="mb-3">
              <Form.Control
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                placeholder='Nowe hasło'
                type={showPass2 ? "text" : "password"}
                name='new_password'
                required
              />
              <InputGroup.Text id="inputGroup-sizing-default" onClick={handleShowPass2}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                  <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                  <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                </svg>
              </InputGroup.Text>
            </InputGroup>

            <Button variant="success" type="submit">
              Zmień hasło
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default ChangePassModal;