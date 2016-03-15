import React from 'react'
import ReactDOM from 'react-dom'
import { Input, Panel, Button, Navbar, NavbarBrand, Nav, NavItem, NavDropdown, MenuItem } from 'react-bootstrap';
import  '../styles/app.less'
import * as jQuery from 'jquery'
import * as io from 'socket.io-client'

var socket = io.connect('http://' + document.domain + ':' + location.port);
var connections = [];

// Then we delete a bunch of code from App and
// add some <Link> elements...
class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            connected:'',
            msg:'initial'
        };
    }

    componentDidMount(){
        console.log('exampleComponent mounted');
        socket.on('connect', this._connected);
        socket.on('ready', this._ready);
        socket.on('zeromq', this._zeromq);
    }

    _connected(){
        socket.emit("hello", {connection_attempt: connections.length});
        console.log("connected");
    }

    _ready = (data) => {
        this.setState({connected:"Socket.IO connected to Flask at "+ data.ready});
        console.log("ready");
    }

    _zeromq = (data) => {
        this.setState({msg:data});
        socket.emit("zeromq");
        console.log("zeromq");
    }

    render() {
        return (
            <div className="container-fluid">
                <Navbar>
                    <NavbarBrand>Flask ReactJS</NavbarBrand>
                    <Nav>
                        <NavItem eventKey={1} href="#">with a hint of Socket.IO and ZeroMQ</NavItem>
                    </Nav>
                </Navbar>

                <div className="row">
                    <Panel header="monitor in" bsStyle="success">
                        <h1> Martin says: {this.state.msg}</h1>
                        <h1> connection is: {this.state.connected}</h1>
                    </Panel>
                </div>
            </div>
        )
    }
}


ReactDOM.render(<App />, document.getElementById('app-container'));
