import os
import inspect
import sys

from jinja2 import Template, Environment, PackageLoader, select_autoescape


class BaseCommand(object):
    def __init__(self, *args, **kwargs):
        self.__name__ = inspect.currentframe().f_code.co_name
        self.command_env = Environment(
            loader=PackageLoader('xmlcommands', os.path.join('templates', 'commands')),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.response_env = Environment(
            loader=PackageLoader('xmlcommands', os.path.join('templates', 'responses')),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.command_template = self.command_env.get_template(self.__name__ + ".xml")
        self.command_render_dict = {}
        self.response_template = self.response_env.get_template(self.__name__ + ".txt")
        self.response_render_dict = {}
        self.proc_dir = os.path.join(os.path.basename(__file__), '..', 'lowell_proc05')
        self.bin_dir = os.path.join(self.proc_dir, 'bin')
        self.command_producer = 'producer'
        self.command_consumer = 'consumer'
        self.command_producer_full_path = os.path.join(self.bin_dir, self.command_producer)
        self.command_consumer_full_path = os.path.join(self.bin_dir, self.command_consumer)
        self.command_producer_message_file = os.path.join(self.proc_dir, 'message.dat')

    def response(self):
        return self.response_template.render(**self.response_render_dict)

    def execute_command(self):
        self.save_command_xml()
        os.system(self.command_producer)
        return self.response()

    def save_command_xml(self):
        command_xml = self.command_template.render(**self.command_render_dict)
        with open(self.generate_save_name(), 'w') as f:
            f.write(command_xml)
        with open(self.command_producer_message_file, 'w') as f:
            f.write(command_xml)

    def generate_save_name(self):
        return self.__name__


class GetCurrentStatus(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
