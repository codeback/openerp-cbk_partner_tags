# -*- encoding: utf-8 -*-
##############################################################################
#
#    res_partner
#    Copyright (c) 2013 Codeback Software S.L. (http://codeback.es)    
#    @author: Miguel García <miguel@codeback.es>
#    @author: Javier Fuentes <javier@codeback.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from datetime import datetime, timedelta
from openerp.tools.translate import _

class res_partner(osv.osv):
    """añadimos los nuevos campos"""
    
    _name = "res.partner"
    _inherit = "res.partner"

    def _get_tags(self, cr, uid, ids, field_names, arg, context=None):
        """
        Gets information from related models for updating purposes       
        """    
        vals={}
        for partner in self.browse(cr,uid,ids):
            vals[partner.id] = {}

            hasChannel = False
            hasDistribution = False

            for category in partner.category_id:
                root = self._get_root_parent(category)

                if root.name == u'Canal':
                    hasChannel = True
                    vals[partner.id]['tag_channel'] = category.id

                if root.name == u'Distribución':
                    hasDistribution = True
                    vals[partner.id]['tag_distribution'] = category.id

            if hasChannel == False:
                vals[partner.id]['tag_channel'] = None

            if hasDistribution == False:
                vals[partner.id]['tag_distribution'] = None


        return vals

    def _get_root_parent(self, category):
        
        if category.parent_id:
            return self._get_root_parent(category.parent_id)
        else:
            return category

    _columns = {   
        'tag_channel': fields.function(_get_tags,
                          multi=True,
                          string=u'Canal',
                          type='many2one',
                          relation='res.partner.category'),
        'tag_distribution': fields.function(_get_tags,
                          multi=True,
                          string=u'Distribución',
                          type='many2one',
                          relation='res.partner.category')
    }

