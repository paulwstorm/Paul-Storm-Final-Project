import React from 'react';
import { Component } from 'react'
import './selectLevel.css'

class SelectLevel extends Component{
  render() {
    return (
      <div>
          <div>Please Select Your Level:</div>
                  <form action="http://localhost:5005/login" method="post">
          <div>
            <label>Username:</label>
            <input type="text" name="username" value="username"/>
          </div>
          <div>
            <label>Password:</label>
            <input type="password" name="password" value="password"/>
          </div>
          <div>
            <input type="submit" value="Log In"/>
          </div>
        </form>
      </div>
    )
  }
}

export default SelectLevel;