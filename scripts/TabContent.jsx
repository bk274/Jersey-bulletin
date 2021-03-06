import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import CommentBlock from './Comments_React/CommentBlock';
import TabWidgets from './TabWidgets';
import ThemeContext from './ThemeContext';

export default function TabContent({
    myName, loggedIn, currTab, myLoginType, myEmail, hasDiscussion,
}) {
    const colorTable = {
        purple: '#9c27b0',
        blue: '#00bbff',
        white: '#f5f5f5',
        green: '#4caf50',
        red: '#f44336',
        orange: '#ff9800',
    };

    const { contextImage, contextColor } = React.useContext(ThemeContext);
    const [image] = contextImage;
    const [color] = contextColor;
    const [style, setStyle] = useState();

    useEffect(() => {
        if (image === '') setStyle({ backgroundColor: `${colorTable[color]}` });
        else setStyle({ backgroundImage: `url(${image})` });
    }, [image, color]);

    return (
        <div className="tab-content" style={style}>
            <TabWidgets currTab={currTab} />
            { hasDiscussion && (
            <CommentBlock
              currTab={currTab}
              myName={myName}
              loggedIn={loggedIn}
              myEmail={myEmail}
              myLoginType={myLoginType}
            />
) }
        </div>
    );
}

TabContent.propTypes = {
    myName: PropTypes.string.isRequired,
    loggedIn: PropTypes.bool.isRequired,
    myEmail: PropTypes.string.isRequired,
    myLoginType: PropTypes.string.isRequired,
    currTab: PropTypes.string.isRequired,
    hasDiscussion: PropTypes.bool.isRequired,
};
