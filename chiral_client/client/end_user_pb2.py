# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: end_user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x65nd_user.proto\x12\x0f\x63hiral_end_user\"8\n\x10RequestAcceptJob\x12\x13\n\x0brequirement\x18\x01 \x01(\t\x12\x0f\n\x07\x64ivisor\x18\x02 \x01(\r\"<\n\x0eReplyAcceptJob\x12\x10\n\x06job_id\x18\x01 \x01(\tH\x00\x12\x0f\n\x05\x65rror\x18\x02 \x01(\tH\x00\x42\x07\n\x05reply\"#\n\x10RequestJobStatus\x12\x0f\n\x07job_ids\x18\x01 \x03(\t\"\xa0\x01\n\x0eReplyJobStatus\x12?\n\x08statuses\x18\x01 \x03(\x0b\x32-.chiral_end_user.ReplyJobStatus.StatusesEntry\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x1a/\n\rStatusesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x08\n\x06_error\"\"\n\x10RequestJobResult\x12\x0e\n\x06job_id\x18\x01 \x01(\t\"?\n\x0eReplyJobResult\x12\x0f\n\x07outputs\x18\x01 \x03(\t\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_error2\x88\x02\n\rChiralEndUser\x12Q\n\tAcceptJob\x12!.chiral_end_user.RequestAcceptJob\x1a\x1f.chiral_end_user.ReplyAcceptJob\"\x00\x12Q\n\tJobStatus\x12!.chiral_end_user.RequestJobStatus\x1a\x1f.chiral_end_user.ReplyJobStatus\"\x00\x12Q\n\tJobResult\x12!.chiral_end_user.RequestJobResult\x1a\x1f.chiral_end_user.ReplyJobResult\"\x00\x42.\n\x16\x63om.chiral.client.grpcB\x0c\x43hiralClientP\x01\xa2\x02\x03HLWb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'end_user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.chiral.client.grpcB\014ChiralClientP\001\242\002\003HLW'
  _REPLYJOBSTATUS_STATUSESENTRY._options = None
  _REPLYJOBSTATUS_STATUSESENTRY._serialized_options = b'8\001'
  _REQUESTACCEPTJOB._serialized_start=35
  _REQUESTACCEPTJOB._serialized_end=91
  _REPLYACCEPTJOB._serialized_start=93
  _REPLYACCEPTJOB._serialized_end=153
  _REQUESTJOBSTATUS._serialized_start=155
  _REQUESTJOBSTATUS._serialized_end=190
  _REPLYJOBSTATUS._serialized_start=193
  _REPLYJOBSTATUS._serialized_end=353
  _REPLYJOBSTATUS_STATUSESENTRY._serialized_start=296
  _REPLYJOBSTATUS_STATUSESENTRY._serialized_end=343
  _REQUESTJOBRESULT._serialized_start=355
  _REQUESTJOBRESULT._serialized_end=389
  _REPLYJOBRESULT._serialized_start=391
  _REPLYJOBRESULT._serialized_end=454
  _CHIRALENDUSER._serialized_start=457
  _CHIRALENDUSER._serialized_end=721
# @@protoc_insertion_point(module_scope)