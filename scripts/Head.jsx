import React, { useState } from 'react';
import PropTypes from 'prop-types';
import LoggedIn from './Auth_React/LoggedIn';
import HeadTitle from './HeadTitle';
import LoginModal from './Auth_React/LoginModal';
import FixedPlugin from './FixedPlugin';
import Navbar from './Navbar';

export default function Head({ logIn, loggedIn, headerClass }) {
    const [display, setDisplay] = useState('none');
    const [ppic, updatePpic] = useState('');
    const [userName, updateUserName] = useState('');

    const handleClick = () => {
        setDisplay('block');
    };

    function setProfilePic({ url, name }) {
        updatePpic(() => url);
        updateUserName(() => name);
    }

    if (loggedIn) {
        return (
            <div className={`sticky shadow ${headerClass}`}>
                <div className="Head">
                    <HeadTitle />
                    <FixedPlugin />
                    <LoggedIn profilePic={ppic} userName={userName} />
                </div>
                <Navbar />
            </div>
        );
    }

    return (
        <div className={`sticky shadow ${headerClass}`}>
            <div className="Head">
                <HeadTitle />
                <FixedPlugin />
                <button onClick={handleClick} type="button" className="login-button">Log In</button>
                <LoginModal
                  logIn={logIn}
                  setProfilePic={setProfilePic}
                  display={display}
                  setDisplay={setDisplay}
                />
            </div>
            <Navbar />
        </div>
    );
}

Head.propTypes = {
    logIn: PropTypes.func.isRequired,
    loggedIn: PropTypes.bool.isRequired,
    headerClass: PropTypes.string.isRequired,
};
