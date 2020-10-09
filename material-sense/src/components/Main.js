import React, { Component } from "react";
import withStyles from "@material-ui/styles/withStyles";
import { withRouter } from "react-router-dom";
import CssBaseline from "@material-ui/core/CssBaseline";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Topbar from "./Topbar";
import SimpleReactivePieChart from "./SimpleReactivePieChart";
import SimpleReactiveBarChart from "./SimpleReactiveBarChart";
import ResponsiveContainer from 'recharts/lib/component/ResponsiveContainer';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

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
    marginTop: 5,
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
    marginBottom: 15,
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
    getStartedDialog: false,
    chartscope: 'all',
    dailyData: [],
    dailyDemo: [],
    dailyTrend: [],
    dailyTrendOrig: []
  };

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

  handleChange = event => {
    var v = event.target.value;
    var newState = (v === 'all' ? this.state.dailyTrendOrig[0] : v === '2wk' ? this.state.dailyTrendOrig[2] : this.state.dailyTrendOrig[1]);
    //var newState = this.state.dailyTrendOrig[2];
    this.setState({ chartscope: v, dailyTrend: newState });
  };

  componentDidMount() {
    fetch("data/dailyData.json")
    .then(res => res.json())
    .then(data => {
      console.log(data);
      this.setState({ ...this.state, dailyData: data })
    });
    fetch("data/dailyTrend.json")
    .then(res => res.json())
    .then(data => {
      console.log(data);
      this.setState({ ...this.state, dailyTrend: data, dailyTrendOrig: [data, data.slice(Math.max(data.length - 60, 1)),data.slice(Math.max(data.length - 14, 1))]}) 
      });
    fetch("data/dailyDemo.json")
    .then(res => res.json())
    .then(data => {
      console.log(data);
      this.setState({ ...this.state, dailyDemo: data })
    });
  }

  render() {
    const { classes } = this.props;
    return (
      <React.Fragment>
        <CssBaseline />
        <Topbar />
        <div className={classes.root}>
          <Grid container justify="center">
            <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                      New in Tokyo
                    </Typography>
                    <Typography variant="body2" display="inline">
                     {this.state.dailyData['NewTokyoCase']} &nbsp; 
                    </Typography>
                    <Typography variant="body2" color="error" display="inline">
                    {(this.state.dailyData['TokyoCaseChange'] > 0) ? '+' : '' } {this.state.dailyData['TokyoCaseChange']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                      7 Day Avg TK
                    </Typography>
                    <Typography variant="body2" gutterBottom display="inline">
                      {this.state.dailyData['TokyoCaseAvg7d']} &nbsp; 
                    </Typography>
                    <Typography variant="body2" color="error" display="inline">
                      {(this.state.dailyData['TokyoCaseAvgDiff'] > 0) ? '+' : ''} {this.state.dailyData['TokyoCaseAvgDiff']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Total Open TK
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                    {this.state.dailyData['TokyoCase']}
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Japan Cases
                    </Typography>
                    <Typography variant="body2" gutterBottom display="inline">
                     {this.state.dailyData['JapanCase']} &nbsp; 
                     </Typography>
                     <Typography variant="body2" color="error" display="inline">
                      + {this.state.dailyData['NewJapanCase']} <br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid item xs={4} md={2}>
                <Paper className={classes.paper}>
                  <div className={classes.box}>
                    <Typography style={{ textTransform: "uppercase" }} color="secondary" gutterBottom>
                    Death Watch
                    </Typography>
                    <Typography variant="body2" gutterBottom>
                    Coming Soon!<br/>
                    </Typography>
                  </div>
                </Paper>
              </Grid>
              <Grid container item xs={12}>
                <Grid item xs={12}>
                  <Paper className={classes.paper}>
                    <div>
                      <div className={classes.box}>
                        <Typography color="secondary" gutterBottom>
                          Daily New Case Counts
                        </Typography>
                      </div>
                      <div>
                        <ResponsiveContainer width="99%" height={225}>
                          <LineChart width={600} height={300} data={this.state.dailyTrend}
                            margin={{
                              top: 5, right: 5, left: 5, bottom: 5,
                            }}
                          >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis orientation="right"/>
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="Tokyo" stroke="#8884d8" activeDot={{ r: 8 }} />
                            <Line type="monotone" dataKey="7dayAvg" stroke="#ff3344" dot={false} activeDot={false} />
                          </LineChart>                            
                        </ResponsiveContainer>
                        <FormControl component="fieldset">
                          <FormLabel component="legend">Timeframe</FormLabel>
                          <RadioGroup name="tf" value={this.state.chartscope} onChange={this.handleChange} row >
                            <FormControlLabel value="all" control={<Radio />} label="All" />
                            <FormControlLabel value="2mo" control={<Radio />} label="2 Month" />
                            <FormControlLabel value="2wk" control={<Radio />} label="2 Weeks " />
                          </RadioGroup>
                        </FormControl>
                      </div>
                    </div>
                  </Paper>
                </Grid>
              </Grid>
              <Grid container justify="center">
                <Grid spacing={2} alignItems="center" justify="center" container className={classes.grid}>
                  <Grid item xs={12} md={6}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                            Gender Breakdown Tokyo (vs -1 day)
                          </Typography>
                        </div>
                        <div>
                          <SimpleReactivePieChart data={this.state.dailyDemo.slice(0,2)} />
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Paper className={classes.paper}>
                      <div>
                        <div className={classes.box}>
                          <Typography color="secondary" gutterBottom>
                          Age Breakdown Tokyo (vs -1 day)
                          </Typography>
                        </div>
                        <div>
                          <SimpleReactiveBarChart data={this.state.dailyDemo.slice(2,12)} />
                        </div>
                      </div>
                    </Paper>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </div>
      </React.Fragment>
    );
  }
}

export default withRouter(withStyles(styles)(Main));
