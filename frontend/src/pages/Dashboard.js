import React, {useContext, useState, useRef} from 'react';
import AuthContext from '../context/AuthContext';


const DashboardPage = () => {
    // Set initial values
    let {user, authToken} = useContext(AuthContext)
    let [error, setError] = useState(null);
    let [create, setCreate] = useState(false);


    let checkLink = async (e) => {
        e.preventDefault();
        // Check given link
        let response = await fetch(`/api/links/exists?url=${e.target.url.value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authToken
            }
        });

        // Get response
        let data = await response.json();

        if(response.status === 422){
            setError('Wprowadzono błędy url.');
            return;
        }else if(response.status === 400){
            setError('Wprowadzony link nie istnieje.');
            return;
        }else if(response.status === 200){
            if(error){
                setError(null);
            }
            setCreate(true);
            return;
        }
        
    };

    const inputRef = useRef(null);

    let createLink = async () => {
        // Create link
        let response = await fetch(`/api/links/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authToken
            },
            body: JSON.stringify({url: inputRef.current.value})
        });

        if (response.status === 201){
            console.log(response.status);
            setCreate(false);
            setError(null);
            inputRef.current.value = '';
        }
    };


    return (
        <div className="h-100 container">
            {user && <h1 className='pb-5 my-5'>Cześć {user.username}</h1>}
            <form onSubmit={checkLink} className='mb-5 pb-5'>
                <div className='w-100 d-flex flex-column justify-content-center align-items-center'>
                    {error ? (
                        <div className="w-100 d-flex flex-column align-items-center">
                            <input
                              type="text"
                              className="form-control is-invalid form-control-lg mx-auto w-100"
                              id="validationServerUsername"
                              aria-describedby="inputGroupPrepend3 validationServerUsernameFeedback"
                              name='url'
                              placeholder="Sprawdź url"
                              required
                            />
                            <div id="validationServerUsernameFeedback" className="invalid-feedback">
                                {error}
                            </div>
                            <button
                              type='submit'
                              className="btn btn-success btn-lg mt-3 px-3 py-2 w-100"
                              style={{maxWidth: 200}}>Sprawdź</button>
                        </div>
                    ): (create ? (
                            <div className='w-100 d-flex flex-column align-items-center'>
                                <input
                                  ref={inputRef}
                                  className="form-control form-control-lg is-valid mx-auto w-100"
                                  type="text"
                                  placeholder='Sprawdz url'
                                  name="url" 
                                  required
                                />
                                <div className="valid-feedback">
                                    Link jest poprawny.
                                </div>
                                <div className='d-flex gap-2'>
                                    <button
                                      type='submit'
                                      className="btn btn-success btn-lg mt-3 px-3 py-2 w-100"
                                      style={{maxWidth: 200}}>Sprawdź</button>
                                    <div
                                      onClick={createLink}
                                      className="btn btn-success btn-lg mt-3 px-3 py-2 w-100"
                                      style={{maxWidth: 200}}>Dodaj</div>
                                </div>
                            </div>
                        ): (
                            <div className='w-100 d-flex flex-column align-items-center'>
                                <input
                                  className="form-control form-control-lg mx-auto w-100"
                                  type="text"
                                  name="url"
                                  placeholder="Sprawdź url"
                                  required
                                />
                                <button
                                  type='submit'
                                  className="btn btn-success btn-lg mt-3 px-3 py-2 w-100"
                                  style={{maxWidth: 200}}>Sprawdź</button>
                            </div>
                            
                        )
                    )}
                </div>
            </form>




            <div className='w-100 d-flex flex-column justify-content-center align-items-center'>
                <h2 className='mt-5 pb-2'>Samochody</h2>
                <div className='w-100 table-responsive'>
                    <table className="table border border-2 rounded-3">
                        <thead>
                            <tr>
                                <th scope="col">Link</th>
                                <th scope="col">Osoba</th>
                                <th scope="col">Data</th>
                            </tr>
                        </thead>
                        <tbody className='table-group-divider'>
                            <tr>
                                <td><a className='link-underline link-underline-opacity-0' href='https://www.example.com'>https://www.example.com</a></td>
                                <td>Ktoś</td>
                                <td>22.12.2023 15:00</td>
                            </tr>
                        </tbody>
                    </table>
                    <nav aria-label="Page navigation example">
                        <ul className="pagination justify-content-center">
                            <li className="page-item disabled">
                                <a className="page-link">Cofnij</a>
                            </li>
                            <li className="page-item"><a className="page-link" href="#">1</a></li>
                            <li className="page-item"><a className="page-link" href="#">2</a></li>
                            <li className="page-item"><a className="page-link" href="#">3</a></li>
                            <li className="page-item">
                                <a className="page-link" href="#">Następna</a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;