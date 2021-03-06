import React from 'react';
import PropTypes from 'prop-types';
import RouteTab from './RouteTab';

export default function Body({
    myName, myEmail, myLoginType, loggedIn,
}) {
    return (
        <div className="Body">
            <RouteTab
              myName={myName}
              loggedIn={loggedIn}
              myEmail={myEmail}
              myLoginType={myLoginType}
            />
        </div>
    );
}

Body.propTypes = {
    myName: PropTypes.string.isRequired,
    myEmail: PropTypes.string.isRequired,
    myLoginType: PropTypes.string.isRequired,
    loggedIn: PropTypes.bool.isRequired,
};
