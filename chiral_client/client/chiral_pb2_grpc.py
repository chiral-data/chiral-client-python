# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import chiral_pb2 as chiral__pb2


class ChiralStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UserInitialize = channel.unary_unary(
                '/chiral.Chiral/UserInitialize',
                request_serializer=chiral__pb2.RequestUserInitialize.SerializeToString,
                response_deserializer=chiral__pb2.ReplyUserInitialize.FromString,
                )
        self.UserSubmitJob = channel.unary_unary(
                '/chiral.Chiral/UserSubmitJob',
                request_serializer=chiral__pb2.RequestUserSubmitJob.SerializeToString,
                response_deserializer=chiral__pb2.ReplyUserSubmitJob.FromString,
                )
        self.UserGetJobStatus = channel.unary_unary(
                '/chiral.Chiral/UserGetJobStatus',
                request_serializer=chiral__pb2.RequestUserGetJobStatus.SerializeToString,
                response_deserializer=chiral__pb2.ReplyUserGetJobStatus.FromString,
                )
        self.UserSendMonitorAction = channel.unary_unary(
                '/chiral.Chiral/UserSendMonitorAction',
                request_serializer=chiral__pb2.RequestUserSendMonitorAction.SerializeToString,
                response_deserializer=chiral__pb2.ReplyUserSendMonitorAction.FromString,
                )
        self.UserSubmitAppJob = channel.unary_unary(
                '/chiral.Chiral/UserSubmitAppJob',
                request_serializer=chiral__pb2.RequestUserSubmitAppJob.SerializeToString,
                response_deserializer=chiral__pb2.ReplyUserSubmitAppJob.FromString,
                )
        self.UserGetCreditPoints = channel.unary_unary(
                '/chiral.Chiral/UserGetCreditPoints',
                request_serializer=chiral__pb2.RequestUserGetCreditPoints.SerializeToString,
                response_deserializer=chiral__pb2.ReplyUserGetCreditPoints.FromString,
                )


class ChiralServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UserInitialize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserSubmitJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserGetJobStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserSendMonitorAction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserSubmitAppJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserGetCreditPoints(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChiralServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UserInitialize': grpc.unary_unary_rpc_method_handler(
                    servicer.UserInitialize,
                    request_deserializer=chiral__pb2.RequestUserInitialize.FromString,
                    response_serializer=chiral__pb2.ReplyUserInitialize.SerializeToString,
            ),
            'UserSubmitJob': grpc.unary_unary_rpc_method_handler(
                    servicer.UserSubmitJob,
                    request_deserializer=chiral__pb2.RequestUserSubmitJob.FromString,
                    response_serializer=chiral__pb2.ReplyUserSubmitJob.SerializeToString,
            ),
            'UserGetJobStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.UserGetJobStatus,
                    request_deserializer=chiral__pb2.RequestUserGetJobStatus.FromString,
                    response_serializer=chiral__pb2.ReplyUserGetJobStatus.SerializeToString,
            ),
            'UserSendMonitorAction': grpc.unary_unary_rpc_method_handler(
                    servicer.UserSendMonitorAction,
                    request_deserializer=chiral__pb2.RequestUserSendMonitorAction.FromString,
                    response_serializer=chiral__pb2.ReplyUserSendMonitorAction.SerializeToString,
            ),
            'UserSubmitAppJob': grpc.unary_unary_rpc_method_handler(
                    servicer.UserSubmitAppJob,
                    request_deserializer=chiral__pb2.RequestUserSubmitAppJob.FromString,
                    response_serializer=chiral__pb2.ReplyUserSubmitAppJob.SerializeToString,
            ),
            'UserGetCreditPoints': grpc.unary_unary_rpc_method_handler(
                    servicer.UserGetCreditPoints,
                    request_deserializer=chiral__pb2.RequestUserGetCreditPoints.FromString,
                    response_serializer=chiral__pb2.ReplyUserGetCreditPoints.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chiral.Chiral', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Chiral(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UserInitialize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chiral.Chiral/UserInitialize',
            chiral__pb2.RequestUserInitialize.SerializeToString,
            chiral__pb2.ReplyUserInitialize.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserSubmitJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chiral.Chiral/UserSubmitJob',
            chiral__pb2.RequestUserSubmitJob.SerializeToString,
            chiral__pb2.ReplyUserSubmitJob.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserGetJobStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chiral.Chiral/UserGetJobStatus',
            chiral__pb2.RequestUserGetJobStatus.SerializeToString,
            chiral__pb2.ReplyUserGetJobStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserSendMonitorAction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chiral.Chiral/UserSendMonitorAction',
            chiral__pb2.RequestUserSendMonitorAction.SerializeToString,
            chiral__pb2.ReplyUserSendMonitorAction.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserSubmitAppJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chiral.Chiral/UserSubmitAppJob',
            chiral__pb2.RequestUserSubmitAppJob.SerializeToString,
            chiral__pb2.ReplyUserSubmitAppJob.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserGetCreditPoints(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chiral.Chiral/UserGetCreditPoints',
            chiral__pb2.RequestUserGetCreditPoints.SerializeToString,
            chiral__pb2.ReplyUserGetCreditPoints.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)