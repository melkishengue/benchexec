# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.benchexec
import benchexec.model
import benchexec.tooladapter
import benchexec.tools
import benchexec.util


class VcloudBenchmarkBase(benchexec.benchexec.BenchExec):
    """
    An extension of BenchExec that supports executing the benchmarks in the
    VerifierCloud (internal project at https://gitlab.com/sosy-lab/software/verifiercloud/).
    """

    def create_argument_parser(self):
        parser = super(VcloudBenchmarkBase, self).create_argument_parser()
        vcloud_args = parser.add_argument_group("Options for using VerifierCloud")
        vcloud_args.add_argument(
            "--vcloud",
            dest="cloud",
            action="store_true",
            help="Use VerifierCloud to execute benchmarks.",
        )

        vcloud_args.add_argument(
            "--vcloudMaster",
            dest="cloudMaster",
            metavar="HOST",
            help="Sets the master host of the VerifierCloud instance to be used. If this is a HTTP URL, the web interface is used.",
        )

        vcloud_args.add_argument(
            "--vcloudPriority",
            dest="cloudPriority",
            metavar="PRIORITY",
            help="Sets the priority for this benchmark used in the VerifierCloud. Possible values are IDLE, LOW, HIGH, URGENT.",
        )

        vcloud_args.add_argument(
            "--vcloudCPUModel",
            dest="cpu_model",
            type=str,
            default=None,
            metavar="CPU_MODEL",
            help="Only execute runs in the VerifierCloud on CPU models that contain the given string.",
        )

        vcloud_args.add_argument(
            "--vcloudUser",
            dest="cloudUser",
            metavar="USER[:PWD]",
            help="The user (and password) for the VerifierCloud (if using the web interface).",
        )

        vcloud_args.add_argument(
            "--revision",
            dest="revision",
            metavar="(tags/<tag name>|branch_name)[:(HEAD|head|<revision number>)]",
            default="trunk:HEAD",
            help="The svn revision of CPAchecker to use (if using the web interface of the VerifierCloud).",
        )

        vcloud_args.add_argument(
            "--justReprocessResults",
            dest="reprocessResults",
            action="store_true",
            help="Do not run the benchmarks. Assume that the benchmarks were already executed in the VerifierCloud and the log files are stored (use --startTime to point the script to the results).",
        )

        vcloud_args.add_argument(
            "--vcloudClientHeap",
            dest="cloudClientHeap",
            metavar="MB",
            default=100,
            type=int,
            help="The heap-size (in MB) used by the VerifierCloud client. A too small heap-size may terminate the client without any results.",
        )

        vcloud_args.add_argument(
            "--vcloudSubmissionThreads",
            dest="cloud_threads",
            default=5,
            type=int,
            help="The number of threads used for parallel run submission (if using the web interface of the VerifierCloud).",
        )

        vcloud_args.add_argument(
            "--vcloudPollInterval",
            dest="cloud_poll_interval",
            metavar="SECONDS",
            default=5,
            type=int,
            help="The interval in seconds for polling results from the server (if using the web interface of the VerifierCloud).",
        )
        vcloud_args.add_argument(
            "--zipResultFiles",
            dest="zipResultFiles",
            action="store_true",
            help="Packs all result files on the worker into a zip file before file transfer (add this flag if a large number of result files is generated).",
        )
        vcloud_args.add_argument(
            "--cgroupAccess",
            dest="cgroupAccess",
            action="store_true",
            help="Allows the usage of cgroups inside the execution environment. This is useful e.g. if a tool wants to make use of resource limits for subprocesses it spawns.",
        )
        vcloud_args.add_argument(
            "--vcloudAdditionalFiles",
            dest="additional_files",
            metavar="FILE_OR_PATH",
            nargs="*",
            type=str,
            help="Specify files or paths that shall also be transferred and be made available to the run in the cloud.",
        )

        return parser

    def check_existing_results(self, benchmark):
        if not self.config.reprocessResults:
            super(VcloudBenchmarkBase, self).check_existing_results(benchmark)