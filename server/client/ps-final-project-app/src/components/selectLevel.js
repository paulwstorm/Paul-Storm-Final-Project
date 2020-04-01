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
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 1</Button>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 2</Button>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 3</Button>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 4</Button>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 5</Button>
              <Button variant = "secondary" type="submit" value="Log In" className="level-button" block>Level 6</Button>
              <div className="usernamePassword">
                <label>Username:</label>
                <input type="text" value="username"/>
              </div>
              <div className="usernamePassword">
                <label>Password:</label>
                <input type="password" value="password"/>
              </div>
            </form>
          </Col>
          <Col xs = {4}></Col>
        </Row>
      </div>
    )
  }
}

export default SelectLevel;