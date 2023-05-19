import React from 'react';
import ReactDOM from 'react-dom/client';
import {createBrowserRouter, RouterProvider} from 'react-router-dom'
import './index.css';
import NavBar from './routes/NavBar';
import ErrorPage from "./error-page";
import Recents from './pages/Recents'
import Watching from './pages/Watching'
import Login from './pages/Login'
import Register from './pages/Register'

const router = createBrowserRouter([
  {
    path: "/",
    element: <NavBar />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "recents/",
        element: <Recents />,
      },
      {
        path: 'watching/',
        element: <Watching username={'zirolet'}/>,
      },
      {
        path: 'login/',
        element: <Login />,
      },
      {
        path: 'register/',
        element: <Register />,
      },
    ]
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <div>
    <RouterProvider router={router} />
  </div>
);