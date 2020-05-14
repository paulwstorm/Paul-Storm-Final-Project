import React from 'react';
import { Component } from 'react'
import { Button, Row, Col } from 'react-bootstrap'
import './userPage.css'
import Header from "./header.js"

class UserPage extends Component{
    render() {
        return (
            <div>
            <Header />
                <Row>
                    <Col xs={4}></Col>
                    <Col className={"user-page-buttons"} xs={4}>
                        <div><Button className={"my-clozes"} href="/user/clozes"> My Clozes</Button></div>
                        <div><Button className={"my-words"} href="/user/words">My Words</Button></div>
                    </Col>
                    <Col xs={4}></Col>
                </Row>
            </div>
        )
    }

}

export default UserPage