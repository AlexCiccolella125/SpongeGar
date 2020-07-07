import React from 'react';
import {
    Drawer,
    DrawerHeader,
    DrawerTitle,
    DrawerSubtitle,
    DrawerContent,
    DrawerAppContent
} from '@rmwc/drawer';
import '@rmwc/drawer/styles';
import {List, ListItem} from '@rmwc/list';
import '@rmwc/list/styles';

const MyDrawer: React.FC<any> = ({open, content}) => {

    return (
        <>
            <div style={{ overflow: 'hidden', position: 'relative' }}>
                <Drawer dismissible open={open}>
                    <DrawerHeader>
                        <DrawerTitle>RED BOT</DrawerTitle>
                        <DrawerSubtitle>Commands</DrawerSubtitle>
                    </DrawerHeader>
                    <DrawerContent>
                        <List>
                            <ListItem>Music</ListItem>
                            <ListItem>Banking</ListItem>
                            <ListItem>Other stuff..</ListItem>
                        </List>
                    </DrawerContent>
                </Drawer>
                <DrawerAppContent
                    style={{ minHeight: '15rem', padding: '1rem' }}
                >
                    {content}
                </DrawerAppContent>
            </div>
        </>
    );
}

export default MyDrawer;
