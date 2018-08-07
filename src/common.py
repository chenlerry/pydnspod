#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Help:
    
"""

import tornado.ioloop
import tornado.web
import pif
import os
import json
from apicn import *

DomainID = {'domainA': '66117180', 'domainB': '65189308', 'domainC': '66094815'}

def server_instance():
    """

    :return:
    """
    api_id = ''
    api_token = ''
    token = "%s,%s" % (api_id, api_token)
    return token


class DomainListHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        """
        下个版本可以考虑自动填充id到字典作为global使用
        :return:
        """
        token = server_instance()
        api = DomainList(token=token)
        domains = api().get("domains")
        len_domain = len(list(domains))
        for name in range(0, len_domain):
            self.write("domain: %s, id: %s" % (domains[name]['name'], domains[name]['id']) + "\n")


class RecordListHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        token = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            api = RecordList(DomainID['%s' % domain], token=token)
            records = api().get("records")
            len_record = len(list(records))
            for i in range(0, len_record):
                self.write("{type:<10} {address:^20} {name:^20} {cordid:^20} {ttl:^20}".format(type=records[i].get('type'),
                                                                                  address=records[i].get('value'),
                                                                                  name=records[i].get('name'),
                                                                                  cordid=records[i].get('id'),
                                                                                  ttl=records[i].get('ttl')) + "\n")


class RecordCreateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        token = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            short_addr = self.get_argument('short_addr')
            a_record = self.get_argument('a_record')
            try:
                api = RecordCreate(a_record, "A", u'默认'.encode("utf8"), short_addr, 600, domain_id=DomainID['%s' % domain], token=token)
                result = api()
                self.write('{"errno": "%s", "result": "%d", "errmsg": "%s"}' % (0, 200, result['status']['message']))
            except Exception as e:
                result = eval(str(e))
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "%s" }' % (1, 500, result['status']['message']))


class RecordRemoveHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        token = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            a_record = self.get_argument('a_record')
            domain_id = DomainID['%s' % domain]
            record_list = {}
            api = RecordList(DomainID['%s' % domain], token=token)
            records = api().get("records")
            len_record = len(list(records))
            for i in range(0, len_record):
                rekey = name=records[i].get('name')
                reid = cordid=records[i].get('id')
                record_list['%s' % rekey] = '%s' % reid
            try:
                record_id = record_list['%s' % a_record]
                api = RecordRemove(record_id, token=token, domain_id=domain_id)
                result = api()
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "%s" }' % (0, 200, result['status']['message']))
            except Exception as e:
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "" }' % (0, 500))


class RecordIPUpdateHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def post(self):
        """

        :return:
        """
        token = server_instance()
        if self.request.arguments:
            domain = self.get_argument('domain')
            a_record = self.get_argument('a_record')
            short_addr = self.get_argument('short_addr')
            if not short_addr:
                short_addr = pif.get_public_ip('ident.me')
            domain_id = DomainID['%s' % domain]
            record_list = {}
            api = RecordList(DomainID['%s' % domain], token=token)
            records = api().get("records")
            len_record = len(list(records))
            for i in range(0, len_record):
                rekey = name=records[i].get('name')
                reid = cordid=records[i].get('id')
                record_list['%s' % rekey] = '%s' % reid
            try:
                record_id = record_list['%s' % a_record]
                api = RecordModify(record_id, sub_domain=a_record, record_type="A", record_line=u'默认'.encode("utf8"), value=short_addr, ttl=600, domain_id=domain_id, token=token)
                result = api()
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "%s" }' % (0, 200, result['status']['message']))
            except Exception as e:
                self.write('{ "errno": "%s", "result": "%d",  "errmsg": "" }' % (0, 500))
