import React, { useEffect, useState } from 'react';
import { Item, Placeholder, Image } from 'semantic-ui-react';
import { nanoid } from 'nanoid';
import { Socket } from '../Socket';
import WidgetTitle from '../WidgetTitle';

export default function NewsList() {
    const [news, setNews] = useState(() => [{}, {}, {}, {}, {}]);
    const [loading, setLoading] = useState(() => true);

    useEffect(() => {
        Socket.on('news', (data) => {
            setNews(data);
            setLoading(false);
        });

        Socket.emit('get news');
    }, []);

    return (
        <div className="widget">
            <WidgetTitle title="News" />
            <Item.Group className="news-group">
                {news.map((item) => (
                    <Item className="news-wrapper" key={nanoid()}>
                        <Item.Image size="tiny" className="news-image">
                            {loading ? (
                                <Placeholder className="news-image">
                                    <Placeholder.Image />
                                </Placeholder>
                            ) : (
                                <Image src={item.image} className="news-image" />
                            )}
                        </Item.Image>
                        <Item.Content>
                            {loading ? (
                                <Placeholder fluid>
                                    <Placeholder.Header>
                                        <Placeholder.Line />
                                    </Placeholder.Header>
                                    <Placeholder.Paragraph>
                                        <Placeholder.Line />
                                        <Placeholder.Line />
                                        <Placeholder.Line />
                                        <Placeholder.Line />
                                    </Placeholder.Paragraph>
                                </Placeholder>
                            ) : (
                                <>
                                    <Item.Header as="a" href={item.url}>{item.title}</Item.Header>
                                    <Item.Description className="news-description">{item.description}</Item.Description>
                                </>
                            )}
                        </Item.Content>
                    </Item>
                ))}
            </Item.Group>
        </div>
    );
}
