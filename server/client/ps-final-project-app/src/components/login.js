import React from 'react';
import { Component } from 'react'
import './login.css'

class Login extends Component{
  render() {
    return (
      <div>
            <form action="http://localhost:5005/login" method="post">
            <div>
                <label>Username:</label>
                <input type="text" name="username"/>
            </div>
            <div>
                <label>Password:</label>
                <input type="password" name="password"/>
            </div>
            <div>
                <input type="submit" value="Log In"/>
            </div>
            </form>
      </div>
    )
  }
}

export default Login;