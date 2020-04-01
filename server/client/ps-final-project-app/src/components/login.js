import React from 'react';
import { Component } from 'react'
import './login.css'

class Login extends Component{
  render() {
    return (
      <div>
       <h3>Logged In</h3>
       <a href="http://localhost:5005/test">click here!</a>
      </div>
    )
  }
}

export default Login;