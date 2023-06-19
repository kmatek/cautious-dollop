import React, {useContext, useState, useRef, useEffect} from 'react';
import AuthContext from '../context/AuthContext';
import moment from 'moment';


const DashboardPage = () => {
    // Set initial values
    let {user, authToken} = useContext(AuthContext)
    let [error, setError] = useState(null);
    let [create, setCreate] = useState(false);
    let [links, setLinks] = useState([]);
    let [loadingLinks, setLoadingLinks] = useState(false);
    let [nextPage, setNextPage] = useState(null);
    let [previousPage, setPreviousPage] = useState(null);


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
        if(response.status === 422){
            setError('Wprowadzono błędy url.');
            return;
        }else if(response.status === 400){
            setError('Wprowadzony link już istnieje.');
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

    let getLinks = async () => {
        // Get links
        let response = await fetch(`/api/links/?size=7`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authToken
            }
        });

        // Get response
        let data = await response.json();

        if(response.status === 200){
            setLinks(data);
            setLoadingLinks(true);
            // Get pagination links
            if(data.links.next){
                setNextPage(data.links.next);
            }
            if(data.links.previous){
                setPreviousPage(data.links.previous);
            }
        }

    };

    let getNextPage = async () => {
        // Get links
        let response = await fetch(nextPage, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authToken
            }
        });

        // Get response
        let data = await response.json();

        if(response.status === 200){
            setLinks(data);
            // Get pagination links
            if(data.links.next){
                setNextPage(data.links.next);
            }
            if(data.links.prev){
                setPreviousPage(data.links.prev);
            }
        }
    };

    let getPrevPage = async () => {
        // Get links
        let response = await fetch(previousPage, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': authToken
            }
        });

        // Get response
        let data = await response.json();

        if(response.status === 200){
            setLinks(data);
            // Get pagination links
            if(data.links.next){
                setNextPage(data.links.next);
            }
            if(data.links.prev){
                setPreviousPage(data.links.prev);
            }
        }
    };

    const convertToGMTPlus2 = (utcDate) => {
        const utcMoment = moment.utc(utcDate);
        const convertedMoment = utcMoment.utcOffset('+0200');
        return convertedMoment.format('YYYY-MM-DD HH:mm:ss');
    };

    useEffect(() => {
        getLinks();
    }, []);

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
                            {loadingLinks && links ? (
                                links.items?.map(link => (
                                    <tr key={link._id}>
                                        <td><a className='link-underline link-underline-opacity-0' href={link.url}>{link.url}</a></td>
                                        <td>{link.added_by}</td> <td>{convertToGMTPlus2(link.date_added)}</td>
                                    </tr>))
                                ): (
                                    <tr>
                                        <td colSpan={3} className='text-center h3'>Pobieram dane...</td>
                                    </tr>
                                )
                            }
                        </tbody>
                    </table>

                    {loadingLinks && links.links ? (
                        <nav aria-label="Page navigation example">
                            <ul className="pagination justify-content-center">
                                {links.links.prev ? (
                                <li className="page-item">
                                    <a className="page-link" onClick={getPrevPage}>Poprzednia strona</a>
                                </li>
                                ): (<li className="page-item disabled">
                                        <a className="page-link" href="#">Poprzednia strona</a>
                                    </li>
                                )}

                                {links.links.next ? (
                                <li className="page-item">
                                    <a className="page-link" onClick={getNextPage}>Następna strona</a>
                                </li>
                                ): (<li className="page-item disabled">
                                        <a className="page-link" href="#">Następna strona</a>
                                    </li>
                                )}
                            </ul>
                        </nav>
                    ): null}
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;