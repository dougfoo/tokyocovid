import React, { Component } from "react";
import withStyles from "@material-ui/styles/withStyles";
import { withRouter } from "react-router-dom";
import CssBaseline from "@material-ui/core/CssBaseline";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Button from "@material-ui/core/Button";
import Topbar from "./Topbar";
import SimpleReactiveChart from "./SimpleReactiveChart";
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

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
    const demoData = [
      { name: 'M/F', m: 4000, f: 2400, },
      { name: 'Age <> 40', yg: 3000, old: 1398, },
      { name: 'Tokyo / Ex', tk: 2000, ex:
       9800, },
    ];

    const dailyTrend = [
      { name: 'Aug 12', tk: 330, os: 140, },
      { name: 'Aug 13', tk: 210, os: 180, },
      { name: 'Aug 14', tk: 150, os: 150, },
      { name: 'Aug 15', tk: 288, os: 190, },
      { name: 'Yesterday', tk: 313, os: 139, },
      { name: 'Today', tk: 188, os: 198, },
    ];

    const dailyData = 
      { 
        'NewTokyoCase': 315,
        'TokyoCase': 1525,
        'NewJapanCase': 1231,
        'NewJapanDeath': 131,
        'JapanCase': 51242,
        'JapanDeath': 3432
      };    

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
                    {dailyData['NewTokyoCase']} - (delta ^)
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
                    {dailyData['TokyoCase']}
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={12} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    All Japan
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                      New Cases: {dailyData['NewJapanCase']} <br/>
                      New Deaths: {dailyData['NewJapanDeath']} <br/>
                      Total Cases: {dailyData['JapanCase']} <br/>
                      Total Deaths: {dailyData['JapanDeath']} <br/>
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
                            Daily New Case Counts
                          </Typography>
                          <Typography variant="body1" gutterBottom>
                            (Tokyo tk, Osaka os)
                          </Typography>
                        </div>
                        <div>
                          <ResponsiveContainer width="99%" height={225}>
                            <LineChart width={600} height={300} data={dailyTrend}
                              margin={{
                                top: 5, right: 5, left: 5, bottom: 5,
                              }}
                            >
                              <CartesianGrid strokeDasharray="3 3" />
                              <XAxis dataKey="name" />
                              <YAxis />
                              <Tooltip />
                              <Legend />
                              <Line type="monotone" dataKey="tk" stroke="#8884d8" activeDot={{ r: 8 }} />
                              <Line type="monotone" dataKey="os" stroke="#82ca9d" />
                            </LineChart>                            
                          </ResponsiveContainer>
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                  <Grid item xs={4}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                            Demographics
                          </Typography>
                          <Typography variant="body1" gutterBottom>
                          Gender, Age, Tokyo vs Japan
                          </Typography>
                        </div>
                        <div>
                          <SimpleReactiveChart data={demoData} />
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
