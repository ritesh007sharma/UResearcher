import React from 'react';
import clsx from 'clsx';
import { useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import InputBase from '@material-ui/core/InputBase';
import Divider from '@material-ui/core/Divider';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import { fade, makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import SearchIcon from '@material-ui/icons/Search';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import HomeIcon from '@material-ui/icons/Home';
import InfoIcon from '@material-ui/icons/Info';
import SettingsIcon from '@material-ui/icons/Settings';
import FeedbackIcon from '@material-ui/icons/Feedback';

import { withStyles } from "@material-ui/core/styles";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import Link from '@material-ui/core/Link';



/* StyledMenu */
const StyledMenu = withStyles({
})(props => (
    <Menu
        getContentAnchorEl={null}
        anchorOrigin={{
            vertical: "bottom",
            horizontal: "center"
        }}
        transformOrigin={{
            vertical: "top",
            horizontal: "center"
        }}
        {...props}
    />
));

const StyledMenuItem = withStyles(theme => ({
    root: {
        "&:focus": {
            backgroundColor: 'teal',
            /* backgroundColor: theme.palette.primary.main, */
            "& .MuiListItemIcon-root, & .MuiListItemText-primary": {
                color: theme.palette.common.white
            }
        }
    }
}))(MenuItem);


const useStyles = makeStyles(theme => ({
    root: {
    },
    menuButton: {
        marginLeft: theme.spacing(1),
    },
    title: {
        display: 'none',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },
    searchWrap: {
        marginLeft  : 'auto',
        marginRight : 'auto'
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(1),
            width: 'auto',
        },
    },
    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            width: 250,
            '&:focus': {
                width: 330,
            },
        },
    },


    appBar: {
        transition: theme.transitions.create(['margin', 'width'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
        }),
    },
    

}));

export default function SearchAppBar({searchValueInput, placeholderInput, enableSearchBar}) {

    var searchValue = searchValueInput;
    var placeholder = placeholderInput;

    const classes = useStyles();

    const theme = useTheme();
    const [open, setOpen] = React.useState(false);

    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };

    const handleSearch = (e) => {
        searchValue = event.target.value;
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        search(searchValue);
    };

    const search = (keywords) => {
        window.location.href = "/search?query=" + keywords;
    };

    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = event => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };


    return (
        <div className={classes.root}>
            <AppBar
                style={{ background: 'teal' }}
                className={clsx(classes.appBar, )}
            >
                <Toolbar>
                    <Typography className={classes.title} variant="h6" noWrap>
                        <a href="/">
                            <img className="m-2" src="static/images/UResearcher_circle.png" width="43" />
                        </a>
                    </Typography>
                    <div className={classes.searchWrap}>
                        {enableSearchBar ? (
                            <div className={classes.search}>
                                <div className={classes.searchIcon}>
                                    <SearchIcon />
                                </div>
                                <form onSubmit={handleSubmit}>
                                    <InputBase
                                        placeholder={placeholder ? placeholder : "Search…"}
                                        defaultValue={searchValue}
                                        classes={{
                                            root: classes.inputRoot,
                                            input: classes.inputInput,
                                        }}
                                        inputProps={{ 'aria-label': 'search', spellCheck : 'true' }}
                                        onChange={handleSearch}
                                    />
                                </form>
                            </div>
                        ): null}
                    </div>
                    <IconButton
                        edge="start"
                        className={classes.menuButton}
                        color="inherit"
                        aria-label="open drawer"
                        onClick={handleClick}
                    >
                        <MenuIcon />
                    </IconButton>
                </Toolbar>
            </AppBar>
            <Toolbar />


            <StyledMenu
                id="customized-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <Link href="/" color="inherit">
                    <StyledMenuItem>
                        <ListItemIcon>
                            <HomeIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="Home" />
                    </StyledMenuItem>
                </Link>
                <Link href="https://github.com/printfer/UResearcher/blob/master/README.md" color="inherit" target="_blank">
                    <StyledMenuItem>
                        <ListItemIcon>
                            <InfoIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="About" />
                    </StyledMenuItem>
                </Link>
                <Divider/>
                <Link href="https://github.com/printfer/UResearcher/issues" color="inherit" target="_blank">
                    <StyledMenuItem>
                        <ListItemIcon>
                            <FeedbackIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="Feedback" />
                    </StyledMenuItem>
                </Link>
                {/*
                <Divider/>
                <Link href="/settings" color="inherit">
                    <StyledMenuItem>
                        <ListItemIcon>
                            <SettingsIcon fontSize="small" />
                        </ListItemIcon>
                        <ListItemText primary="Settings" />
                    </StyledMenuItem>
                </Link>
                */}
            </StyledMenu>

        </div>
    );
}

