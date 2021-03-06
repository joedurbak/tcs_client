from . import commands

COMMANDS = {
    'A': commands.GetCurrentStatus,
    'C': commands.SendDomeStopCommand,
    'D': commands.SendDomeControllerCommand,
    'E': commands.ResetError,
    'F': commands.ExitProgram,
    'G': commands.OpenMirrorCover,
    'H': commands.CloseMirrorCover,
    'I': commands.ClearFocusPositionScaleAValue,
    'J': commands.ClearFocusPositionScaleBValue,
    'K': commands.MoveFocus,
    'L': commands.ReturnToFocusOrigin,
    'M': commands.SendOperationCommandInHorizontalCoordinateSystem,
    'N': commands.SendNullCommand,
    'O': commands.TurnOffControllerPower,
    'P': commands.ChangeOffsetValue,
    'P0': commands.ClearOffsetValue,
    'Q': commands.SendOperationCommandInHorizontalCoordinateSystemOnlyOnce,
    'R': commands.ChangeRotatorThetaFlag,
    'S': commands.StopTelescope,
    'T': commands.MoveTelescopeTargetEquitorialCoordinateSystemAndTrack,
    'U': commands.SetNewPositionIncludingOffsetValue,
    'X': commands.MoveTelescopeToFlatScreenPosition,
    'Y': commands.MoveTelescopeToHomePosition,
    'Z': commands.ZeroSearch,
    'e': commands.AzimuthXZeroSearch,
    'f': commands.AltitudeYZeroSearch,
    'g': commands.RotationThetaZeroSearch,
    'x': commands.TurnOnLinkToDomeMovement,
    'y': commands.TurnOffLinkToDomeMovement,
    'D0': commands.MoveDomeToHomePosition,
    'DL': commands.TurnOnOffDomeLamp,
    'DE': commands.EmergencyDomeStop,
    'DM': commands.MoveDome,
    'DD': commands.UpdateDomePosition,
    'DS': commands.OpenCloseDomeSlit,
    'RE': commands.EmergencyRoofStop,
    'RA': commands.TurnOnOffDomeLamp,
    'RC': commands.OpenCloseRoof,
    'MA': commands.MoveTelescopeBasedOnAbsoluteEncoder,
    'j': commands.MoveFocusToSpecifiedPosition,
    'k': commands.ChangeFocusPositionAValue,
    'ks': commands.ChangeFocusPositionBValue,
    'tcp_error': commands.TCPError,
}


def execute_command(tcp_command="T 23:59:59.9 +89:59:59.9 0.0 0.0 000.0 NONAME"):
    split_command = tcp_command.split()
    command = split_command[0]
    try:
        arguments = split_command[1:]
    except IndexError:
        arguments = None
    try:
        tcs_command = COMMANDS[command](arguments, tcp_command)
    except KeyError:
        tcs_command = COMMANDS['tcp_error'](arguments, tcp_command)
    try:
        return tcs_command.execute_command()
    except Exception as e:
        'Received message {}, but generated error: {}'.format(tcs_command, e)
        return e
