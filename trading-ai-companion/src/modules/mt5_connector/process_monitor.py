"""
MT5 Process Monitor - Complete Implementation
"""

import psutil
import logging
import time
from typing import Dict, Any, List
from datetime import datetime

class MT5ProcessMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.mt5_processes = []
        self.monitoring = False
        self.monitor_thread = None
    
    def find_mt5_processes(self) -> List[Dict[str, Any]]:
        """Find all MT5-related processes"""
        mt5_processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent']):
                try:
                    proc_name = proc.info['name'].lower() if proc.info['name'] else ""
                    proc_exe = proc.info['exe'].lower() if proc.info['exe'] else ""
                    
                    # Check for MT5 processes
                    if ('terminal' in proc_name and 'meta' in proc_name) or \
                       ('metatrader' in proc_name and '5' in proc_name) or \
                       ('terminal' in proc_exe and 'meta' in proc_exe):
                        
                        # Get additional process info
                        try:
                            proc_obj = psutil.Process(proc.info['pid'])
                            create_time = datetime.fromtimestamp(proc_obj.create_time())
                        except:
                            create_time = None
                        
                        mt5_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'exe': proc.info['exe'],
                            'status': proc_obj.status() if 'proc_obj' in locals() else 'unknown',
                            'cpu_percent': proc.info['cpu_percent'],
                            'memory_percent': proc.info['memory_percent'],
                            'create_time': create_time.isoformat() if create_time else None
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                    pass
            return mt5_processes
        except Exception as e:
            self.logger.error(f"Error finding MT5 processes: {e}")
            return []
    
    def monitor_process_health(self, pid: int) -> Dict[str, Any]:
        """Monitor the health of a specific process"""
        try:
            proc = psutil.Process(pid)
            return {
                'pid': pid,
                'status': proc.status(),
                'cpu_percent': proc.cpu_percent(),
                'memory_percent': proc.memory_percent(),
                'memory_info': proc.memory_info()._asdict(),
                'running': proc.is_running(),
                'num_threads': proc.num_threads(),
                'timestamp': datetime.now().isoformat()
            }
        except psutil.NoSuchProcess:
            return {'pid': pid, 'status': 'not_found', 'running': False}
        except Exception as e:
            self.logger.error(f"Error monitoring process {pid}: {e}")
            return {'pid': pid, 'status': 'error', 'running': False}
    
    def get_system_resources(self) -> Dict[str, Any]:
        """Get system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100 if disk.total > 0 else 0
                },
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting system resources: {e}")
            return {}
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting network stats: {e}")
            return {}
    
    def get_mt5_process_stats(self) -> List[Dict[str, Any]]:
        """Get detailed statistics for all MT5 processes"""
        mt5_processes = self.find_mt5_processes()
        stats = []
        
        for proc_info in mt5_processes:
            try:
                pid = proc_info['pid']
                proc_stats = self.monitor_process_health(pid)
                proc_stats.update(proc_info)
                stats.append(proc_stats)
            except Exception as e:
                self.logger.error(f"Error getting stats for process {proc_info.get('pid')}: {e}")
        
        return stats
    
    def check_resource_thresholds(self, thresholds: Dict[str, float] = None) -> Dict[str, Any]:
        """Check if system resources exceed thresholds"""
        if thresholds is None:
            thresholds = {
                'cpu_percent': 80.0,
                'memory_percent': 85.0,
                'disk_percent': 90.0
            }
        
        system_resources = self.get_system_resources()
        alerts = []
        
        if system_resources.get('cpu_percent', 0) > thresholds['cpu_percent']:
            alerts.append({
                'type': 'cpu',
                'level': 'warning',
                'message': f'CPU usage high: {system_resources["cpu_percent"]:.1f}%'
            })
        
        if system_resources.get('memory', {}).get('percent', 0) > thresholds['memory_percent']:
            alerts.append({
                'type': 'memory',
                'level': 'warning',
                'message': f'Memory usage high: {system_resources["memory"]["percent"]:.1f}%'
            })
        
        if system_resources.get('disk', {}).get('percent', 0) > thresholds['disk_percent']:
            alerts.append({
                'type': 'disk',
                'level': 'warning',
                'message': f'Disk usage high: {system_resources["disk"]["percent"]:.1f}%'
            })
        
        return {
            'system_resources': system_resources,
            'alerts': alerts,
            'status': 'ok' if not alerts else 'warning'
        }
    
    def get_process_tree(self, pid: int) -> Dict[str, Any]:
        """Get process tree for a specific process"""
        try:
            proc = psutil.Process(pid)
            children = proc.children(recursive=True)
            
            tree = {
                'pid': pid,
                'name': proc.name(),
                'children': []
            }
            
            for child in children:
                try:
                    tree['children'].append({
                        'pid': child.pid,
                        'name': child.name(),
                        'status': child.status()
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return tree
        except psutil.NoSuchProcess:
            return {'error': 'Process not found'}
        except Exception as e:
            self.logger.error(f"Error getting process tree for {pid}: {e}")
            return {'error': str(e)}
