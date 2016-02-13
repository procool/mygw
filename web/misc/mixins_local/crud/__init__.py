import logging

from models.session import session

class ObjectViewMixin(object):
    def get_model(self, *args, **kwargs):
        return self.model

    def get_queryset_filters(self, qs=None, **kwargs):
        return qs.filter()

    def get_queryset_postfix(self, qs=None, **kwargs):
        return qs

    def get_queryset(self, qs=None, **kwargs):
        if qs is not None:
            return qs

        return session.query(self.get_model())

    def get_queryset_compiled(self, **kwargs):
        if hasattr(self, '__qs_compiled') and self.__qs_compiled is not None:
            return self.__qs_compiled
        qs = self.get_queryset(**kwargs)
        qs = self.get_queryset_filters(qs=qs, **kwargs)
        qs = self.get_queryset_postfix(qs=qs, **kwargs)
        self.__qs_compiled = qs
        return qs

    def close_db_session(self):
        logging.info('Closing DB session...')
        connection = session.connection()
        connection.close()
        session.close_all()
        session.close()

    def prepare(self, *args, **kwargs):
        self.__qs_compiled = None
        r = super(ObjectViewMixin, self).prepare(*args, **kwargs)
        self.close_db_session()
        return r


class ListViewBaseMixin(ObjectViewMixin):

    ## To Override:
    ## list_name = None
    ## model = None

    def get_list_name(self):
        try: return self.list_name
        except: return 'objects'

    def get_context_data(self, **kwargs):
        context = super(ListViewBaseMixin, self).get_context_data(**kwargs)
        context['list_name'] = self.get_list_name()
        context[self.get_list_name()] = list(self.get_queryset_compiled())
        return context

