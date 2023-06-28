import { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Modal from 'react-bootstrap/Modal';

function CreateNewUserModal() {

  const [show, setShow] = useState(false);
  const [showPass, setShowPass] = useState(false);
  const [errorEmail, setErrorEmail] = useState(null);

  const handleClose = () => {
    setShow(false);
    setErrorEmail(null);
  }
  const handleShow = () => setShow(true);
  const handleShowPass = () => setShowPass(!showPass);

  let createNewUserRequest = async (e) => {
    e.preventDefault();

    // Create user
    let response = await fetch('/api/user/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        'password': e.target.password.value,
        'email': e.target.email.value,
        'username': e.target.username.value
      })
    });

    if (!response.ok){
      setErrorEmail('Email jest już zajęty');
    };
    if (response.ok){
        handleClose();
    }
  };

  return (
    <>
      <Button variant="success" onClick={handleShow} style={{maxWidth: 200}}>
        Dodaj użytkownika
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Dodaj użytkownika</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={createNewUserRequest}>
            <Form.Control
                className='mb-3'
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                placeholder="Nazwa użytkownika"
                type='text'
                name='username'
                required
            />

            <InputGroup className="mb-3">
              <Form.Control
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                placeholder="Email"
                type="email"
                name='email'
                className={errorEmail ? "is-invalid" : ""}
                required
              />
              {errorEmail && <div className="invalid-feedback">{errorEmail}</div> }
            </InputGroup>

            <InputGroup className="mb-3">
              <Form.Control
                aria-label="Default"
                aria-describedby="inputGroup-sizing-default"
                placeholder="Hasło"
                type={showPass ? "text" : "password"}
                name='password'
                required
              />
              <InputGroup.Text id="inputGroup-sizing-default" onClick={handleShowPass}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
                  <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                  <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                </svg>
              </InputGroup.Text>
            </InputGroup>

            <Button variant="success" type="submit">
              Dodaj
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
}

export default CreateNewUserModal;