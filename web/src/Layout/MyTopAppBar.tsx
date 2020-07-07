import React from 'react';
import {
    TopAppBar,
    TopAppBarRow,
    TopAppBarSection,
    TopAppBarTitle,
    TopAppBarFixedAdjust,
    TopAppBarNavigationIcon
} from '@rmwc/top-app-bar';
import '@rmwc/top-app-bar/styles';


const MyTopAppBar: React.FC<any> = ({open, setOpen}) => {
    return (
        <>
            <TopAppBar>
                <TopAppBarRow>
                    <TopAppBarSection alignStart>
                        <TopAppBarNavigationIcon icon="menu" onClick={() => setOpen(!open)}/>
                        <TopAppBarTitle>RED</TopAppBarTitle>
                    </TopAppBarSection>
                </TopAppBarRow>
            </TopAppBar>
            <TopAppBarFixedAdjust />
        </>
    )
}

export default MyTopAppBar;
