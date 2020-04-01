import React from 'react';
import { Component } from 'react'
import { Button, Row, Col } from 'react-bootstrap'
import './selectLevel.css'
import Header from "./header.js"

class SelectLevel extends Component{
  render() {
    return (
      <div>
       <Header />        
        <Row>
          <Col xs = {3}></Col>
          <Col xs = {6}>
            <h3 className="selectLevelTitle">Please Select Your Level:</h3>
          </Col>
          <Col xs = {3}></Col>
        </Row>
        <Row>
          <Col xs = {4}></Col>
          <Col xs = {4}>
            <form action="http://localhost:5005/login" method="post">
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" name="username" value="1"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" name="password" value="password"/>
              </div>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 1</Button>
            </form>
            <form action="http://localhost:5005/login" method="post">
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" name="username" value="2"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" name="password" value="password"/>
              </div>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 2</Button>
            </form>
            <form action="http://localhost:5005/login" method="post">
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" name="username" value="3"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" name="password" value="password"/>
              </div>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 3</Button>
            </form>
            <form action="http://localhost:5005/login" method="post">
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" name="username" value="4"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" name="password" value="password"/>
              </div>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 4</Button>
            </form>
            <form action="http://localhost:5005/login" method="post">
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" name="username" value="5"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" name="password" value="password"/>
              </div>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 5</Button>
            </form>
            <form action="http://localhost:5005/login" method="post">
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" name="username" value="6"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" name="password" value="password"/>
              </div>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 6</Button>
            </form>
          </Col>
          <Col xs = {4}></Col>
        </Row>
      </div>
    )
  }
}

export default SelectLevel;