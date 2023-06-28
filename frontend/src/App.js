import { BrowserRouter as Router, Route } from 'react-router-dom'
import LoginPage from './pages/Login';
import DashboardPage from './pages/Dashboard';

import PrivateRoute from './utils/PrivateRoute';
import { AuthProvider} from './context/AuthContext';



const App = () => {
  return (
      <div className="w-100 h-100 d-flex justify-content-center align-items-center">
          <Router>
              <AuthProvider>
                <Route path="/login" exact component={LoginPage} />
                <PrivateRoute path="/" exact component={DashboardPage} />
              </AuthProvider>
          </Router>
      </div>
  );
}

export default App;
