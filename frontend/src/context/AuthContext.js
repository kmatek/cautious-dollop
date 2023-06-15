import { createContext, useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import jwt_decode from "jwt-decode";

const getExpirationTime = (token) => {
    // Get expiration time from token
    let decoded = jwt_decode(token);
    return decoded.exp;
}

const AuthContext = createContext()

export default AuthContext;

export const AuthProvider = ({children}) => {

    // Set initial values
    let [authToken, setAuthToken] = useState(localStorage.getItem('token') ? localStorage.getItem('token') : null);
    let [expirationDate, setExpirationDate] = useState(localStorage.getItem('expirationDate') ? localStorage.getItem('expirationDate') : null);
    let [user, setUser] = useState(localStorage.getItem('user') ? localStorage.getItem('user') : null);
    let [error, setError] = useState(null);
    let [loading, setLoading] = useState(true)

    const history = useHistory()

    // Get user info
    let login = async (e) => {
        e.preventDefault();

        // Get token
        let response = await fetch('/api/user/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'email': e.target.email.value, 'password': e.target.password.value})
        });

        // Set token
        let data = await response.json();
        if (response.ok){
            setAuthToken(`${data.token_type} ${data.access_token}`);
            localStorage.setItem('token',`${data.token_type} ${data.access_token}`);

            // // Set expiration time to half of token expiration time
            const expirationDate = new Date(getExpirationTime(data.access_token) * 1000);
            setExpirationDate(expirationDate.getTime());
            localStorage.setItem('expirationDate', expirationDate.getTime());

            // Get user info
            let response = await fetch('/api/user/me', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${data.token_type} ${data.access_token}`
                }
            });

            // Set user info
            let newData = await response.json();
            if (response.ok){
                // Set loading to false
                if (loading) {
                    setLoading(false);
                }

                localStorage.setItem('user', newData.username);
                setUser(newData);
                history.push('/');
            };

        }else{
            // Set error
            setError(data.detail);
        }
        
    };

    // Clear user info
    let logout = () => {
        setAuthToken(null);
        localStorage.removeItem('token');
        setExpirationDate(null);
        localStorage.removeItem('expirationDate');
        setUser(null);
        localStorage.removeItem('user');
        history.push('/');
    };

    let contextData = {
        user:user,
        authToken:authToken,
        error:error,
        login:login,
    }

    useEffect(()=> {
        // Logout if token expired
        if (expirationDate && new Date().getTime() > parseInt(expirationDate)){
            logout();
        }
    }, [expirationDate])


    return(
        <AuthContext.Provider value={contextData} >
            {children}
        </AuthContext.Provider>
    )
}