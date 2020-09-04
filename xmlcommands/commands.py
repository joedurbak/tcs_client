from jinja2 import Template


class BaseCommand:
    def __init__(self, *args, **kwargs):
        self.tcs_template = ''
        self.tcs_render_dict = {}
        self.tcp_template = 'not implemented yet'
        self.tcp_render_dict = {}

    def tcp_answer(self):
        return Template(self.tcp_template).render(**self.tcp_render_dict)

    def execute_tcs_command(self):
        return self.tcp_answer()


class GetCurrentStatus(BaseCommand):
    pass


class SendDomeStopCommand(BaseCommand):
    pass


class SendDomeControllerCommand(BaseCommand):
    pass


class ResetError(BaseCommand):
    pass


class ExitProgram(BaseCommand):
    pass


class OpenMirrorCover(BaseCommand):
    pass


class CloseMirrorCover(BaseCommand):
    pass


class ClearFocusPositionScaleAValue(BaseCommand):
    pass


class ClearFocusPositionScaleBValue(BaseCommand):
    pass


class MoveFocus(BaseCommand):
    pass


class ReturnToFocusOrigin(BaseCommand):
    pass


class SendOperationCommandInHorizontalCoordinateSystem(BaseCommand):
    pass


class SendNullCommand(BaseCommand):
    pass


class TurnOffControllerPower(BaseCommand):
    pass


class ChangeOffsetValue(BaseCommand):
    pass


class ClearOffsetValue(BaseCommand):
    pass


class SendOperationCommandInHorizontalCoordinateSystemOnlyOnce(BaseCommand):
    pass


class ChangeRotatorThetaFlag(BaseCommand):
    pass


class StopTelescope(BaseCommand):
    pass


class MoveTelescopeTargetEquitorialCoordinateSystemAndTrack(BaseCommand):
    pass


class SetNewPositionIncludingOffsetValue(BaseCommand):
    pass


class MoveTelescopeToFlatScreenPosition(BaseCommand):
    pass


class MoveTelescopeToHomePosition(BaseCommand):
    pass


class ZeroSearch(BaseCommand):
    pass


class AzimuthXZeroSearch(BaseCommand):
    pass


class AltitudeYZeroSearch(BaseCommand):
    pass


class RotationThetaZeroSearch(BaseCommand):
    pass


class TurnOnLinkToDomeMovement(BaseCommand):
    pass


class TurnOffLinkToDomeMovement(BaseCommand):
    pass


class MoveDomeToHomePosition(BaseCommand):
    pass


class TurnOnOffDomeLamp(BaseCommand):
    pass


class EmergencyDomeStop(BaseCommand):
    pass


class MoveDome(BaseCommand):
    pass


class UpdateDomePosition(BaseCommand):
    pass


class OpenCloseDomeSlit(BaseCommand):
    pass


class EmergencyRoofStop(BaseCommand):
    pass


class TurnOnOffAirConditioner(BaseCommand):
    pass


class OpenCloseRoof(BaseCommand):
    pass


class MoveTelescopeBasedOnAbsoluteEncoder(BaseCommand):
    pass


class MoveFocusToSpecifiedPosition(BaseCommand):
    pass


class ChangeFocusPositionAValue(BaseCommand):
    pass


class ChangeFocusPositionBValue(BaseCommand):
    pass
