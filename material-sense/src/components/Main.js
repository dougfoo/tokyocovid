import React, { Component } from "react";
import withStyles from "@material-ui/styles/withStyles";
import { withRouter } from "react-router-dom";
import CssBaseline from "@material-ui/core/CssBaseline";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import InstructionDialog from "./dialogs/InstructionDialog";
import SwipeDialog from "./dialogs/SwipeDialog";

import Topbar from "./Topbar";

const backgroundShape = require("../images/shape.svg");

const styles = theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.grey["100"],
    overflow: "hidden",
    background: `url(${backgroundShape}) no-repeat`,
    backgroundSize: "cover",
    backgroundPosition: "0 400px",
    paddingBottom: 200
  },
  grid: {
    width: 1200,
    marginTop: 40,
    [theme.breakpoints.down("sm")]: {
      width: "calc(100% - 20px)"
    }
  },
  paper: {
    padding: theme.spacing(3),
    textAlign: "left",
    color: theme.palette.text.secondary
  },
  rangeLabel: {
    display: "flex",
    justifyContent: "space-between",
    paddingTop: theme.spacing(2)
  },
  topBar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: 32
  },
  outlinedButtom: {
    textTransform: "uppercase",
    margin: theme.spacing(1)
  },
  actionButtom: {
    textTransform: "uppercase",
    margin: theme.spacing(1),
    width: 152
  },
  blockCenter: {
    padding: theme.spacing(2),
    textAlign: "center"
  },
  block: {
    padding: theme.spacing(2)
  },
  box: {
    marginBottom: 40,
    height: 65
  },
  inlining: {
    display: "inline-block",
    marginRight: 10
  },
  buttonBar: {
    display: "flex"
  },
  alignRight: {
    display: "flex",
    justifyContent: "flex-end"
  },
  noBorder: {
    borderBottomStyle: "hidden"
  },
  loadingState: {
    opacity: 0.05
  },
  loadingMessage: {
    position: "absolute",
    top: "40%",
    left: "40%"
  }
});

class Main extends Component {
  state = {
    learnMoredialog: false,
    getStartedDialog: false
  };

  componentDidMount() {}

  openDialog = event => {
    this.setState({ learnMoredialog: true });
  };

  dialogClose = event => {
    this.setState({ learnMoredialog: false });
  };

  openGetStartedDialog = event => {
    this.setState({ getStartedDialog: true });
  };

  closeGetStartedDialog = event => {
    this.setState({ getStartedDialog: false });
  };

  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        <CssBaseline />
        <Topbar />
        <div className={classes.root}>
          <Grid container justify="center">
            <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
              <Grid item xs={12} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                      New Cases Tokyo
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      Blah blah blah <br /> Today vs Yesterday
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={12} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                      New Deaths Tokyo
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      Blah blah blah <br /> Today vs Yesterday
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={12} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Total Open Tokyo
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      Blah blah blah <br /> Today vs Yesterday
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={12} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Total Deaths Tokyo
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      Blah blah blah <br /> Today vs Yesterday
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={12} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    For All of Japan
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      New Cases <br/>
                      Total Open Cases <br/>
                      Total Deaths
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid container item xs={12}>
                <Grid spacing={4} alignItems="center" justify="center" container className={classes.grid}>
                  <Grid item xs={8}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                            Chart 1
                          </Typography>
                          <Typography variant="body1" gutterBottom>
                            This needs to be a flex height box
                          </Typography>
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                  <Grid item xs={4}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                            Chart 2
                          </Typography>
                          <Typography variant="body1" gutterBottom>
                          This needs to be a flex height box
                          </Typography>
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
            <Grid container item xs={12}>
              <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
                <Grid item xs={12} md={8}>
                  <Paper className={classes.paper}>
                    <div className={classes.box}>
                      <Typography style={{ textTransform: "uppercase" }} color="secondary" >
                        Photo Library of My Dogs
                      </Typography>
                      <Button onClick={this.openDialog} variant="outlined" className={classes.actionButtom}>
                        To Dogs
                      </Button>
                    </div>
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
          {/* <SwipeDialog
            open={this.state.learnMoredialog}
            onClose={this.dialogClose}
          />
          <InstructionDialog
            open={this.state.getStartedDialog}
            onClose={this.closeGetStartedDialog}
          /> */}
        </div>
      </React.Fragment>
    );
  }
}

export default withRouter(withStyles(styles)(Main));
