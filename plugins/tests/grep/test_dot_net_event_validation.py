'''
test_dot_net_event_validation.py

Copyright 2012 Andres Riancho

This file is part of w3af, w3af.sourceforge.net .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
'''

from plugins.tests.helper import PluginTest, PluginConfig


class TestEventValidation(PluginTest):
    
    dot_net_event_validation_url = 'http://moth/w3af/grep/event_validation/'
    
    _run_configs = {
        'cfg1': {
            'target': dot_net_event_validation_url,
            'plugins': {
                'grep': (PluginConfig('dot_net_event_validation'),),
                'crawl': (
                    PluginConfig('web_spider',
                                 ('onlyForward', True, PluginConfig.BOOL)),
                )         
                
            }
        }
    }
    
    def test_found_vuln(self):
        cfg = self._run_configs['cfg1']
        self._scan(cfg['target'], cfg['plugins'])
        vulns = self.kb.get('dot_net_event_validation', 'dot_net_event_validation')
        
        self.assertEquals(3, len(vulns))
        
        EXPECTED_VULNS = set([('event_validation.html', 'decode the viewstate contents.'),
                              ('without_event_validation.html', 'decode the viewstate contents.'),
                              ('without_event_validation.html', 'r should be manually verified.')])
        
        vulns_set = set()
        for vuln in vulns:
            ending = vuln.getDesc(with_id=False)[-30:]
            vulns_set.add( (vuln.getURL().getFileName(), ending ) )

        self.assertEqual( EXPECTED_VULNS,
                          vulns_set)
        
        
        