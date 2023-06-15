import React, {useContext} from 'react';
import AuthContext from '../context/AuthContext';


const DashboardPage = () => {
    let {user} = useContext(AuthContext)
    return (
        <div className="h-100 container">
            {user && <h1 className='pb-5 my-5'>Cześć {user.username}</h1>}
            <form className='mb-5 pb-5'>
                <div className='w-100 d-flex flex-column justify-content-center align-items-center'>
                    <input className="form-control form-control-lg mx-auto w-100" type="text" placeholder="Sprawdź url"/>
                    <button className="btn btn-success btn-lg mt-3 px-3 py-2 w-100" style={{maxWidth: 200}}>Sprawdź</button>
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
                        <ul class="pagination justify-content-center">
                            <li class="page-item disabled">
                                <a class="page-link">Cofnij</a>
                            </li>
                            <li class="page-item"><a class="page-link" href="#">1</a></li>
                            <li class="page-item"><a class="page-link" href="#">2</a></li>
                            <li class="page-item"><a class="page-link" href="#">3</a></li>
                            <li class="page-item">
                                <a class="page-link" href="#">Następna</a>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;