import React from 'react';
import PropTypes from 'prop-types';
import TrafficWidget from './Traffic_React/TrafficWidget';
import NewsList from './News_React/NewsList';
import WeatherModule from './Weather_React/WeatherModule';
import TweetWidget from './Tweet_React/TweetWidget';
import BillsWidget from './Bills_React/BillsWidget';

export default function TabWidgets({ currTab }) {
    if (currTab === 'Commuter') {
        return (
            <div className="tab-widgets-section">
                <WeatherModule />
                <TrafficWidget />
            </div>
        );
    }

    if (currTab === 'Politics') {
        return (
            <div className="tab-widgets-section">
                <TweetWidget />
                <BillsWidget />
            </div>
        );
    }

    return (
        <div className="tab-widgets-section">
            <NewsList />
            <WeatherModule />
        </div>
    );
}

TabWidgets.propTypes = {
    currTab: PropTypes.string.isRequired,
};
