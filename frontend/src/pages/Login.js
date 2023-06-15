import React, { useContext } from 'react';
import AuthContext from '../context/AuthContext';

const LoginPage = () => {
    let { login, error } = useContext(AuthContext);

    return (
        <form onSubmit={login} className="border border-2 rounded p-4 bg-secondary-subtle">
            <h5 className="mb-5">Habibi</h5>
            { error && <div className="alert alert-danger" role="alert">{error}</div>}
            <div className="mb-3">
                <input type="email" name="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Email" defaultValue='' required/>
            </div>
            <div className="mb-3">
                <input type="password" name="password" className="form-control" id="exampleInputPassword1" placeholder="Hasło" defaultValue='' required/>
            </div>
            <button type="submit" className="btn btn-primary">Zaloguj się</button>
        </form>
    );
};

export default LoginPage;