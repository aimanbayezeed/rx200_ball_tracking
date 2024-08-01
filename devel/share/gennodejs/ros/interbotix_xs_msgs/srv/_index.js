
"use strict";

let MotorGains = require('./MotorGains.js')
let TorqueEnable = require('./TorqueEnable.js')
let OperatingModes = require('./OperatingModes.js')
let RegisterValues = require('./RegisterValues.js')
let Reboot = require('./Reboot.js')
let RobotInfo = require('./RobotInfo.js')

module.exports = {
  MotorGains: MotorGains,
  TorqueEnable: TorqueEnable,
  OperatingModes: OperatingModes,
  RegisterValues: RegisterValues,
  Reboot: Reboot,
  RobotInfo: RobotInfo,
};
